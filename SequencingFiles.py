"""
created by Juechen Yang at 2/26/20

"""
import os

class Fastq:
    '''
    class to define a WXS sequencing file
    @:param: file_path
    '''
    def __init__(self, file_path):
        # check if the file exists
        if os.path.isfile(file_path):
            # check if the file is a fastq
            if file_path.lower().endswith(".fastq") or file_path.lower().endswith(".fq"):
                self.__file_path = file_path
            else:
                print(file_path, " is not a fastq file")
        else:
            print(file_path, " does not exist")

    def get_path(self):
        return self.__file_path