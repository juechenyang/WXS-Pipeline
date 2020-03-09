"""
created by Juechen Yang at 2/25/20

"""
import os
import subprocess
from subprocess import run
from StaticPath import StaticPath
#specify the root dir
gtf_file = os.path.join(StaticPath.DataDir, 'gencode.v22.annotation.gtf.gz')
fasta_file = os.path.join(StaticPath.DataDir, 'GRCh38.d1.vd1.fa.tar.gz')

#try to download from GDC
try:
    # execute to download the gtf file
    print("dowloading gtf file")
    run(['wget', '-O', gtf_file, '-P', StaticPath.DataDir,
        'https://api.gdc.cancer.gov/data/25aa497c-e615-4cb7-8751-71f744f9691f'],
        stdout=subprocess.DEVNULL, check=True)

    # execute to download the FASTA file
    print("dowloading FASTA file")
    run(['wget', '-O', fasta_file, '-P', StaticPath.DataDir,
        'https://api.gdc.cancer.gov/data/254f697d-310d-4d7d-a27b-27fbf767a834'],
        stdout=subprocess.DEVNULL, check=True)
except:
    print("dowloading failed, please check the connection")

#extraction process

#extract gtf file
try:
    run(['gunzip', gtf_file], stdout=subprocess.DEVNULL, check=True)
except FileNotFoundError:
    print(" ".join([gtf_file, 'does not exist']))

#extract fasta file
try:
    run(['tar', '-zxvf', fasta_file, '--directory', StaticPath.DataDir], stdout=subprocess.DEVNULL, check=True)
except FileNotFoundError:
    print(" ".join([fasta_file, 'does not exist']))

#remove the fasta tar
os.remove(fasta_file)