"""
created by Juechen Yang at 2/28/20

"""
import os

#make sure the dir exists
def checkout_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)