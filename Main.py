"""
created by Juechen Yang at 2/26/20

"""
from SequencingFiles import Fastq
import subprocess as sb
import argparse
import sys

parser = argparse.ArgumentParser(description='''
************************************************************************************************
Basic description:

Integrated Pipeline for Whole Exome Sequencing

************************************************************************************************
    ''',formatter_class=argparse.RawTextHelpFormatter
)
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('--read1', help='required option, which is used to specify fastq read1. \nPlease use comma to seprate each fastq file if your sample contains multiple files')
requiredNamed.add_argument('--read2', help='required option, which is used to specify fastq read2. \nPlease use comma to seprate each fastq file if your sample contains multiple files')
args = parser.parse_args()

#get the path of two sequencing file
rd1_path = args.read1
rd2_path = args.read2

if not rd1_path or not rd2_path:
    print("missing required pair-end reads")
    sys.exit()



#initialize pair-end reads obj
rd1 = Fastq(rd1_path)
rd2 = Fastq(rd2_path)

#get read length of the sequencing files

##construct the read length command string
read_length_cmd = "{if(NR%4==2) {count++; bases += length} } END{print bases/count}"
read_length = sb.check_output(["awk", read_length_cmd, rd1.get_path()])

#print read length
print(read_length)
