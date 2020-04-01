
from subprocess import check_output
import sys,os,argparse
from StaticPath import StaticPath, Separators
from time import ctime
from SequencingFormats import BAM

parser = argparse.ArgumentParser(description='''
************************************************************************************************
Basic description:

Call mutation from tumor and normal bam

************************************************************************************************

Usage instructions:

    1. if starts from fq then required arguments include:
    --normal_fq1 --normal_fq2 --normal_sample_id --tumor_fq1 --tumor_fq2 --tumor_sample_id
    2. if starts from bam then required arguments include:
    --normal_bam --tumor_bam --normal_sample_id --tumor_sample_id

    ''', formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('--StartsFromBam', default=False, action='store_true')
parser.add_argument('--normal_fq1')
parser.add_argument('--normal_fq2')
parser.add_argument('--tumor_fq1')
parser.add_argument('--tumor_fq2')
parser.add_argument('--normal_sample_id')
parser.add_argument('--tumor_sample_id')
parser.add_argument('--normal_bam')
parser.add_argument('--tumor_bam')
parser.add_argument('--out_dir', default='./outfiles')

args = parser.parse_args()

#get the path of two sequencing file
FromBam = args.StartsFromBam
normal_fq1_path = args.normal_fq1
normal_fq2_path = args.normal_fq2
tumor_fq1_path = args.tumor_fq1
tumor_fq2_path = args.tumor_fq2
normal_sample_id = args.normal_sample_id
tumor_sample_id = args.tumor_sample_id
output_dir = args.out_dir

normal_bam_path = args.normal_bam
tumor_bam_path = args.tumor_bam

if not (normal_sample_id and tumor_sample_id):
    print('please specify both tumor and normal id')
    sys.exit(1)

'''

step1 preprocess tumor and normal bam

'''

if FromBam:
    #if starts from bam
    if not (normal_bam_path and tumor_bam_path):
        print('please specify --tumor_bam and --normal_bam ')
        sys.exit(1)

    print("started preprocess from bams at", ctime())

    # preprocess the normal bam
    normal_out = check_output([sys.executable, "WXS_preprocess.py", "--StartsFromBam", '--bam', normal_bam_path,
                               "--output_dir", output_dir, "--sample_id", normal_sample_id], encoding="UTF-8")
    normal_bam_path = normal_out.split('\n')[-2]
    # build the normal bam object
    normal_bam = BAM(normal_bam_path)

    # preprocess the tumor bam
    tunor_out = check_output([sys.executable, "WXS_preprocess.py", "--StartsFromBam", '--bam', tumor_bam_path,
                               "--output_dir", output_dir, "--sample_id", tumor_sample_id], encoding="UTF-8")

    tumor_bam_path = tunor_out.split('\n')[-2]
    # #build the tumor bam object
    tumor_bam = BAM(tumor_bam_path)
else:
    print("started preprocess from fastq at", ctime())

    # preprocess the normal bam
    normal_out = check_output([sys.executable, "WXS_preprocess.py", "--fq1", normal_fq1_path,
                               "--fq2", normal_fq2_path, "--output_dir", output_dir,
                               "--sample_id", normal_sample_id], encoding="UTF-8")
    normal_bam_path = normal_out.split('\n')[-2]
    # build the normal bam object
    normal_bam = BAM(normal_bam_path)

    # preprocess the tumor bam
    tunor_out = check_output([sys.executable, "WXS_preprocess.py", "--fq1", tumor_fq1_path,
                              "--fq2", tumor_fq2_path, "--output_dir", output_dir,
                              "--sample_id", tumor_sample_id], encoding="UTF-8")

    tumor_bam_path = tunor_out.split('\n')[-2]
    # #build the tumor bam object
    tumor_bam = BAM(tumor_bam_path)












#call mutations based on normal bam and tumor bam
from subprocess import CalledProcessError,run
from GenomeReference import GenomeReference
from tools import checkout_dir
def call_mutation(tumor_bam, normal_bam, out_dir):
    #get sample id
    sample_id = normal_bam.fetch_sample_id()

    vcf_dir = os.path.join(out_dir, 'vcf')
    checkout_dir(vcf_dir)
    case_mutation_vsf = os.path.join(vcf_dir, sample_id+Separators.sample_name_separator+'somatic.vcf.gz')

    cmd = " ".join(['gatk', 'Mutect2', '-R', GenomeReference.get_reference_fasta(), '-I', tumor_bam.get_path(),
                    '-I', normal_bam.get_path(), '-normal', sample_id, '--germline-resource', StaticPath.germline_file,
                    '--panel-of-normals', StaticPath.pon, '-O', case_mutation_vsf])

    try:
        run([cmd], shell=True, check=True)
    except CalledProcessError as e:
        print(e)

    return case_mutation_vsf

call_mutation(tumor_bam, normal_bam, out_dir=output_dir)


'''
used for debug
'''

# #get the path of tumor and normal fastqs
# normal_fq1_path = os.path.join(StaticPath.base_dir, 'FASTQs', 'normal1.fq')
# normal_fq2_path = os.path.join(StaticPath.base_dir, 'FASTQs', 'normal2.fq')
# tumor_fq1_path = os.path.join(StaticPath.base_dir, 'FASTQs', 'tumor1.fq')
# tumor_fq2_path = os.path.join(StaticPath.base_dir, 'FASTQs', 'tumor2.fq')
# tumor_sample_id = "TARGET-30-PALHVD-01A-01W"
# normal_sample_id = "TARGET-30-PALHVD-10A-01W"
#build the normal bam object
# normal_bam = BAM(os.path.join(StaticPath.base_dir, 'out_files',
#             normal_sample_id,'bams', normal_sample_id+'.sorted.merged.markdup.bqsr.bam'))
# tumor_bam = BAM(os.path.join(StaticPath.base_dir, 'out_files', tumor_sample_id,
#             'bams',tumor_sample_id+'.sorted.merged.markdup.bqsr.bam'))