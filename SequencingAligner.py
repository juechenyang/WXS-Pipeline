"""
created by Juechen Yang at 2/26/20

"""
from GenomeReference import GenomeReference
import subprocess as sb
class BWA:
    '''
    BWA Aligner
    '''
    def __init__(self, mode):
        if mode in ['mem', 'aln']:
            self.__mode = mode
        else:
            print(mode, ' mode is not valid')
            import sys
            sys.exit()

    def start_alignment(self, rd1, rd2, outbam):

        ref_fasta = GenomeReference.get_reference_fasta()
        annotation_gtf = GenomeReference.get_annotation_gtf()

        if self.__mode == 'mem':
            # construct bwa command
            cmd = " ".join(["bwa", self.__mode, "-t", "8", "-T", "0", ref_fasta, rd1.get_path(), rd2.get_path(), "|", "samtools", "view", "-Shb", "-o", outbam])
            # a = "bwa mem -t 8 -T 0 -R <read_group> <reference> <fastq_1.fq.gz> <fastq_2.fq.gz> | samtools view -Shb -o <output.bam>"
            try:
                process = sb.run([cmd], shell=True)
                process.check_returncode()
            except sb.CalledProcessError as e:
                print("error was caught, it is ", e.output)
        elif self.__mode == 'aln':
            a = 1







