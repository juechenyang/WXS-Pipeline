"""
created by Juechen Yang at 2/26/20

"""
import os, time,re,sys
import subprocess as sb
import tools
from StaticPath import StaticPath
from GenomeReference import GenomeReference

class Fastq:
    '''
    class to define a WXS sequencing file
    @:param: file_path
    '''
    def __init__(self, file_path):
        #get the absolute path of the fastq
        abs_file_path = os.path.abspath(file_path)
        # check if the file exists
        if os.path.isfile(abs_file_path):
            # check if the file is a fastq
            if abs_file_path.lower().endswith(".fastq") or abs_file_path.lower().endswith(".fq"):
                self.__file_path = abs_file_path
                self.__read_length = None
            else:
                print(abs_file_path, " is not a fastq file")
        else:
            print(abs_file_path, " does not exist")

    def get_path(self):
        return self.__file_path

    # get read length of the sequencing files
    def get_read_length(self):
        if self.__read_length == None:
            print("started calculating length at ", time.ctime(), "...")
            read_length_cmd = "{if(NR%4==2) {count++; bases += length} } END{print bases/count}"
            try:
                read_length = sb.check_output(["awk", read_length_cmd, self.get_path()], encoding='UTF-8')
                read_length = re.sub('\n', '', read_length)
                read_length = float(read_length)
                self.__read_length = read_length
                return read_length
            except sb.CalledProcessError as e:
                print(e.output)
                return False
        else:
            return self.__read_length



class BAM:
    '''
    Class for BAM file
    '''

    def __init__(self, bam_path):

        # converted the path to absolute path
        abs_bam_path = os.path.abspath(bam_path)

        #check if the bam_path is valid
        if os.path.isfile(abs_bam_path):
            # check if the file is a bam
            if abs_bam_path.lower().endswith(".bam"):
                self.__path = abs_bam_path
            else:
                print(abs_bam_path, " is not a bam file")
        else:
            print(abs_bam_path, " does not exist")

    #get the bam path
    def get_path(self):
        return self.__path

    def fetch_sample_id(self):
        # define sample_id
        self.__sample_id = self.__path.split('.')[0]
        return self.__sample_id

    def __get_bqsr_path(self):
        sample_id = self.fetch_sample_id()
        return ".".join([sample_id, "bqsr", "table"])

    #sort the bam file
    def sort_bam(self, create_index=False, keep_origin=False):
        sorted_bam = ".".join([self.__path.split(".bam")[0], "sorted", "bam"])
        try:
            print("started sorting bam at ", time.ctime())
            #construct the command
            cmd = " ".join(['java', '-jar', StaticPath.picard_path, 'SortSam', "CREATE_INDEX="+str(create_index).lower(),
                            'INPUT='+self.__path, 'OUTPUT='+sorted_bam, 'SORT_ORDER=coordinate', 'VALIDATION_STRINGENCY=STRICT'])
            process = sb.run([cmd], shell=True, check=True)

            # Whether to keep original bam
            if keep_origin:
                print(" ".join([self.__path, 'was', 'kept']))
            else:
                os.remove(self.__path)
                print(" ".join([self.__path, 'was', 'removed']))


            return BAM(sorted_bam)
        except:
            print("Internal process of sorting bam got error!")
            return False

    def to_fastq(self):
        '''
        picard solutions
        :return: a list of path indicating two fastqs
        '''
        try:
            print('started converting bam to fastq at ', time.ctime())
            #checkout the fastq dir
            fastq_dir = os.path.join(StaticPath.base_dir, "FASTQs")
            tools.checkout_dir(fastq_dir)
            #sepcify the output fastqs
            out_fq1 = os.path.join(fastq_dir, "aln.end1.fq")
            out_fq2 = os.path.join(fastq_dir, "aln.end2.fq")

            #construct the command
            command = " ".join(["java", '-jar', StaticPath.picard_path, 'SamToFastq', 'I='+self.__path, 'FASTQ='+out_fq1, 'SECOND_END_FASTQ='+out_fq2])
            process = sb.run([command], shell=True, stdout=sb.DEVNULL)
            process.check_returncode()
            print('successfully converted!')
            return [out_fq1, out_fq2]
        except:
            print("oops! converting fastq failed, check the input bam")
            return False


    def merge_bam(self, keep_origin=False, create_index=False):
        merged_bam = ".".join([self.__path.split(".bam")[0], "merged", "bam"])
        print('started merging bam at ', time.ctime())
        cmd = " ".join(['java', '-jar', StaticPath.picard_path, 'MergeSamFiles', 'ASSUME_SORTED=false', 'CREATE_INDEX='+str(create_index).lower(),
                        'INPUT='+self.__path, 'MERGE_SEQUENCE_DICTIONARIES=false', 'OUTPUT='+merged_bam, 'SORT_ORDER=coordinate',
                        'USE_THREADING=true', 'VALIDATION_STRINGENCY=STRICT'])
        try:
            sb.run([cmd], shell=True, check=True)
            # Whether to keep original bam
            if keep_origin:
                print(" ".join([self.__path, 'was', 'kept']))
            else:
                os.remove(self.__path)
                print(" ".join([self.__path, 'was', 'removed']))
            return BAM(merged_bam)
        except:
            print("Internal process of merge bam got error!")


    def mark_duplicate(self, keep_origin=False, create_index=False):
        markdup_bam = ".".join([self.__path.split(".bam")[0], "markdup", "bam"])
        print('started mark duplicate at ', time.ctime())
        cmd = " ".join(['java', '-jar', StaticPath.picard_path, 'MarkDuplicates', 'CREATE_INDEX='+str(create_index).lower(), 'INPUT='+self.__path,
                        'OUTPUT='+ markdup_bam, 'M='+os.path.join(StaticPath.IntermediateDir, 'marked_dup_metrics.txt'),
                        'VALIDATION_STRINGENCY=STRICT'])
        try:
            sb.run([cmd], shell=True, check=True)
            # Whether to keep original bam
            if keep_origin:
                print(" ".join([self.__path, 'was', 'kept']))
            else:
                os.remove(self.__path)
                print(" ".join([self.__path, 'was', 'removed']))
            return BAM(markdup_bam)
        except:
            print("Internal process of mark duplicate got error!")

    def make_BQSR(self):
        print("start making bqsr table at "+time.ctime())
        bqsr_table = self.__get_bqsr_path()
        cmd = " ".join(['gatk', 'BaseRecalibrator', '-I', self.__path, '-R', GenomeReference.get_reference_fasta(),
                        '--known-sites', StaticPath.dbsnp, '-O', bqsr_table])
        try:
            sb.run([cmd], shell=True, check=True)
        except:
            print('Internal process of make BQSR failed')

    def apply_BQSR(self, create_index=False, keep_origin=False):
        bqsr_bam = ".".join([self.__path.split(".bam")[0], "bqsr", "bam"])
        print("start applying bqsr to output bam at "+time.ctime())
        bqsr_table = self.__get_bqsr_path()

        #check if bqsr table is ready
        if not os.path.isfile(bqsr_table):
            print(" ".join([bqsr_table, 'is not a prepared']))
            sys.exit(1)

        cmd = " ".join(['gatk', 'ApplyBQSR', '-R', GenomeReference.get_reference_fasta(), '-I', self.__path,
                        '--bqsr-recal-file', bqsr_table, '--create-output-bam-index', str(create_index).lower(),
                        '-O', bqsr_bam])
        try:
            sb.run([cmd], shell=True, check=True)
            # Whether to keep original bam
            if keep_origin:
                print(" ".join([self.__path, 'was', 'kept']))
            else:
                os.remove(self.__path)
                print(" ".join([self.__path, 'was', 'removed']))
        except sb.CalledProcessError as e:
            print('Internal of apply bqsr failed')
            print(e)

        return BAM(bqsr_bam)


