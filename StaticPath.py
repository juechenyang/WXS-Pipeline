"""
created by Juechen Yang at 3/5/20

"""
import os,tools
class StaticPath:
    # define the base dir
    base_dir = os.path.dirname(os.path.realpath(__file__))
    # get picard tool location
    picard_path = os.path.join(base_dir, "tools", "picard.jar")
    # define intermediate file dir
    IntermediateDir = os.path.join(base_dir, "IntermediateFiles")
    tools.checkout_dir(IntermediateDir)
    #define the output dirs
