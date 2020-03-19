"""
created by Juechen Yang at 2/26/20

"""
from SequencingFormats import Fastq, BAM
from StaticPath import StaticPath
import argparse
import sys,time,os, tools
import SequencingAligner as SeqAligner
from GenomeReference import GenomeReference
from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser(description='''
************************************************************************************************
Basic description:

Integrated Pipeline for Whole Exome Sequencing

************************************************************************************************

Usage instructions:

    1. if you start this pipeline from a bam file, please activate bam mode use "--StartsFromBam" and specify the path of your bam by using "--bam".
    In this mode, "--fq1" and "--fq2" command will be automatically ignored
    
    2. if you start this pipeline from pair-end fastq files, please ignore both "--StartsFromBam" and "--bam" parameters
    and directly specify the path of "--fq1" and "--fq2"
    
    ''',formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('--StartsFromBam', default=False, action='store_true', help="Whether starts the pipeline from bam file, if yes then --bam must be specified")
parser.add_argument('--bam', help='bam input')
parser.add_argument('--fq1', help='fastq read1')
parser.add_argument('--fq2', help='fastq read2')
args = parser.parse_args()

#get the path of two sequencing file
FromBam = args.StartsFromBam
rd1_path = args.fq1
rd2_path = args.fq2
bam_path = args.bam

#check if index has been build
all_files_in_data_dir = [f for f in listdir(StaticPath.DataDir)
                         if isfile(join(StaticPath.DataDir, f)) and f.endswith('sa')]
if len(all_files_in_data_dir) == 0:
    print("index has not been built, try to rebuild")
    GenomeReference.create_index()


if FromBam:
    print("started from bam at ", time.ctime())
    # check if required bam is missing
    if not bam_path:
        print("please specify --bam option")
        sys.exit()
    else:
        '''
        step1: Convert the bam to pair-end fastq
        '''
        #initialize bam instance
        bam = BAM(bam_path)
        #convert the bam to pair-end fastqs
        fastqs = bam.to_fastq()

        #check if fastq was successfully converted
        if fastqs:
            #get the path of converted fastq
            rd1_path = fastqs[0]
            rd2_path = fastqs[1]
        else:
            print('error, fastq was not prepared')
            sys.exit()
else:
    # if not starts from bam, fq1 and fq2 must be specified
    if not (rd1_path and rd2_path):
        print("missing required fastqs, please specify")
        sys.exit()
    else:
        print("started from fastq at ", time.ctime())


'''

Step2: align the pair-end reads to reference genome

'''

rd1 = Fastq(rd1_path)
rd2 = Fastq(rd2_path)

out_dir = os.path.join(StaticPath.base_dir, "outputs")
out_bam_dir = os.path.join(out_dir, "bams")
tools.checkout_dir(out_bam_dir)
out_bam = os.path.join(out_bam_dir  , "realigned.bam")


#check if read length is greater than or equals to 70
print("started alignment at ", time.ctime())
if rd1.get_read_length() >= 70:
    print("read length is ", str(rd1.get_read_length()), ", So bwa use mem mode")
    aligner = SeqAligner.BWA('mem')
    aligned_bam = aligner.start_alignment(rd1, rd2, out_bam)

else:
    print("read length is ", str(rd1.get_read_length()), ", So bwa use aln mode")
    aligner = SeqAligner.BWA('aln')
    aligned_bam = aligner.start_alignment(rd1, rd2, out_bam)

'''

Step3 sort bam

'''
#sort the aligned bam
sorted_bam = aligned_bam.sort_bam()


'''

Step4: merge bam

'''

merged_bam = sorted_bam.merge_bam()

'''

Step5: mark duplicate

'''
markdup_bam = merged_bam.mark_duplicate()
print(markdup_bam.get_path())
'''

Step6:create index and diction for reference genome

'''
if not isfile(GenomeReference.reference_index):
    GenomeReference.index_fasta()
if not isfile(GenomeReference.reference_dict):
    GenomeReference.make_diction()


'''

Step7: BaseRecalibration

'''
markdup_bam.make_BQSR()
bqsr_bam = markdup_bam.apply_BQSR(create_index=True)

print(bqsr_bam.get_path())

'''

Step8: Mutech2 calling mutation

'''














