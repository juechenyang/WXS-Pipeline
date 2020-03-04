"""
created by Juechen Yang at 2/26/20

"""
import os, time,re
import subprocess as sb

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
        #define the base dir
        self.__base_dir = os.path.dirname(os.path.realpath(__file__))

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

    #sort the bam file
    def __sort_bam(self):
        try:
            print("started sorting bam at ", time.ctime())
            sort_bam = os.path.join(self.__base_dir, "input_sorted.bam")
            command = "samtools sort -n " + self.__path + " -o " + sort_bam
            process = sb.run([command], shell=True)
            process.check_returncode()
            return sort_bam
        except:
            print("sort process error")
            return False

    def to_fastq(self):
        #sort bam
        sorted_bam = self.__sort_bam()
        #check if sort was successful
        if(sorted_bam):
            #convert bam
            try:
                print('started converting bam to fastq at ', time.ctime())
                out_fq1 = os.path.join(self.__base_dir, "aln.end1.fq")
                out_fq2 = os.path.join(self.__base_dir, "aln.end2.fq")
                command = "bedtools bamtofastq -i "+ sorted_bam +" -fq " + out_fq1 + " -fq2 "+ out_fq2
                process = sb.run([command], shell=True)
                process.check_returncode()
                print('successfully converted!')
                #remove the sorted bam file
                os.remove(sorted_bam)
                #return the output fastqs
                return [out_fq1, out_fq2]
            except:
                print("oops! some errors happen, please try it again")
                return False
        else:
            print("error, bam was not sorted")
            return False


