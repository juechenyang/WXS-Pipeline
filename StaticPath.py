"""
created by Juechen Yang at 3/5/20

"""
import os
from tools import checkout_dir
class StaticPath:
    # define the base dir
    base_dir = os.path.dirname(os.path.realpath(__file__))
    # get picard tool location
    picard_path = os.path.join(base_dir, "tools", "picard.jar")

    # define intermediate file dir
    IntermediateDir = os.path.join(base_dir, "IntermediateFiles")
    checkout_dir(IntermediateDir)

    # define intermediate file dir
    DataDir = os.path.join(base_dir, "data")
    checkout_dir(DataDir)

    #define dbsnp location
    dbsnp = os.path.join(DataDir, "common_all_20170710.vcf")

    # define germline resource location
    germline_file = os.path.join(DataDir, "af-only-gnomad.hg38.vcf.gz")

    #define panel of normal
    pon = os.path.join(DataDir, "1000g_pon.hg38.vcf.gz")

    #define the tmp dir
    tmp_dir = os.path.join(base_dir, 'tmp')
    checkout_dir(tmp_dir)

class Separators:

    #sample name separator
    sample_name_separator = ','



