"""
created by Juechen Yang at 2/26/20

"""
from GenomeReference import GenomeReference
from SequencingFormats import BAM
from StaticPath import StaticPath
import os,time, tools
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

        if self.__mode == 'mem':
            # construct bwa command
            cmd = " ".join(["bwa", self.__mode, "-t", "8", "-T", "0", ref_fasta, rd1.get_path(), rd2.get_path(),
                            "|", "samtools", "view", "-Shb", "-o", outbam])
            try:
                process = sb.run([cmd], shell=True)
                process.check_returncode()
                return BAM(outbam)
            except sb.CalledProcessError as e:
                print("error was caught, it is ", e.output)
        elif self.__mode == 'aln':
            IntermediateDir = os.path.join(StaticPath.base_dir, "IntermediateFiles")
            tools.checkout_dir(IntermediateDir)
            sai1_path = os.path.join(IntermediateDir, 'sai_1.sai')
            sai2_path = os.path.join(IntermediateDir, 'sai_2.sai')
            # cmd = " ".join(["bwa", self.__mode, "-t", "8", ref_fasta, rd1.get_path(), ">", sai1_path])
            cmd = " ".join(["bwa", self.__mode, "-t", "8", ref_fasta, rd1.get_path(), ">", sai1_path, "&&",
                            "bwa", self.__mode, "-t", "8", ref_fasta, rd2.get_path(), ">", sai2_path, "&&",
                            "bwa", "sampe", ref_fasta, sai1_path, sai2_path, rd1.get_path(), rd2.get_path(),
                            "|", "samtools", "view", "-Shb", "-o", outbam])
            try:
                process = sb.run([cmd], shell=True, check=True)
                return BAM(outbam)
            except sb.CalledProcessError as e:
                print("error was caught, it is ", e.output)









