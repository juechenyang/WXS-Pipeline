"""
created by Juechen Yang at 2/28/20

"""
import os

class GenomeReference:
    '''
    class locates reference genome files
    '''
    base_dir = os.path.dirname(os.path.realpath(__file__))
    genome_dir = os.path.join(base_dir, 'data')
    # specify the path of reference_fasta and annotation_gtf
    __reference_fasta = os.path.join(genome_dir, 'GRCh38.d1.vd1.fa')
    __annotation_gtf = os.path.join(genome_dir, 'gencode.v22.annotation.gtf')

    @staticmethod
    def get_reference_fasta():
        return GenomeReference.__reference_fasta

    @staticmethod
    def get_annotation_gtf():
        return GenomeReference.__annotation_gtf