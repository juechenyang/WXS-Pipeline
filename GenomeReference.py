"""
created by Juechen Yang at 2/28/20

"""
import os
from StaticPath import StaticPath
from subprocess import run
import subprocess

class GenomeReference:
    '''
    class locates reference genome files
    '''
    # specify the path of reference_fasta and annotation_gtf
    __reference_fasta = os.path.join(StaticPath.DataDir, 'GRCh38.d1.vd1.fa')
    __annotation_gtf = os.path.join(StaticPath.DataDir, 'gencode.v22.annotation.gtf')

    # define the reference index file
    reference_index = os.path.join(StaticPath.DataDir, 'GRCh38.d1.vd1.fa.fai')

    # define the reference dict file
    reference_dict = os.path.join(StaticPath.DataDir, 'GRCh38.d1.vd1.dict')

    @staticmethod
    def get_reference_fasta():
        return GenomeReference.__reference_fasta

    @staticmethod
    def get_annotation_gtf():
        return GenomeReference.__annotation_gtf

    @staticmethod
    def create_index():
        #construct the command
        cmd = " ".join(['bwa', 'index', GenomeReference.__reference_fasta])
        try:
            run([cmd], shell=True, check=True)

        except FileNotFoundError:
            print(" ".join([GenomeReference.__reference_fasta, 'was not found']))

        except subprocess.CalledProcessError:
            print('bwa index got error')

    @staticmethod
    def index_fasta():
        #construct the command
        cmd = " ".join(['samtools', 'faidx', GenomeReference.__reference_fasta])
        #run the command
        try:
            run([cmd], shell=True, check=True)
        except subprocess.CalledProcessError:
            print("index fasta got error")
        except FileNotFoundError:
            print(" ".join([GenomeReference.__reference_fasta, 'was not found']))

    @staticmethod
    def make_diction():
        # construct the command
        cmd = " ".join(['samtools', 'dict', GenomeReference.__reference_fasta, '-o',
                        GenomeReference.__reference_fasta.split(".fa")[0]+'.dict'])
        # run the command
        try:
            run([cmd], shell=True, check=True)
        except subprocess.CalledProcessError:
            print("dict fasta got error")
        except FileNotFoundError:
            print(" ".join([GenomeReference.__reference_fasta, 'was not found']))