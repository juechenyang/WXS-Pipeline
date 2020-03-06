"""
created by Juechen Yang at 2/28/20

"""
import os
import subprocess as sb

#make sure the dir exists
def checkout_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# def call_mutation(bam):
#     bam = BAM()
#     cmd = " ".join()