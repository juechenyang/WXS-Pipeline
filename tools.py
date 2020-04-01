"""
created by Juechen Yang at 2/28/20

"""
import os
#make sure the dir exists
def checkout_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)



# def create_panel_of_normal(normal_bam):
#
#     #fetch the sample id from bam obj
#     sample_id = normal_bam.fetch_sample_id()
#     normal_vcf = os.path.join(StaticPath.IntermediateDir, 'normal.pon.vcf.gz')
#     case_pon_vcf = os.path.join(StaticPath.IntermediateDir, sample_id+NameSeparator.sep+'pon.vcf.gz')
#
#     #step1:
#     cmd = " ".join(['gatk', 'Mutect2', '-R', GenomeReference.get_reference_fasta(), '-I', normal_bam.get_path(),
#                     '-max-mnp-distance 0', '-O', normal_vcf])
#     try:
#         run([cmd], shell=True, check=True)
#     except CalledProcessError as e:
#         print(e)
#
#
#     #step2:
#     cmd = " ".join(['gatk', 'GenomicsDBImport', '-R', GenomeReference.get_reference_fasta(), '-L',
#                     os.path.join(StaticPath.IntermediateDir, 'intervals.interval_list'),
#                     '--genomicsdb-workspace-path pon_db', '-V', normal_vcf])
#     try:
#         run([cmd], shell=True, check=True)
#     except CalledProcessError as e:
#         print(e)
#
#     #step3:
#     cmd = " ".join(['gatk', 'CreateSomaticPanelOfNormals', '-R', GenomeReference.get_reference_fasta(),
#                     '-V', 'gendb://pon_db', '-O', case_pon_vcf])
#
#     return case_pon_vcf