import sys
import os
from DDLify.utility_funcs import print_usage
from DDLify.PhyModel import PhyModel


def setup(argv):
    """
    The setup function should first check and make sure that a filename or directory name has been given as a parameter.
    It then creates blank output files for stg, owner, and amalgamation sql.
    """
    if len(argv) != 2:
        print_usage()
        sys.exit(2)
    else:
        filename = argv[1]

    return filename


def main(filename):
    """
    The main function should check and see if the filename parameter represents a directory or a file.  If it is a file
    then the file should be processed and turned into a physical model, validated, and have DDL created. If it is a
    directory then the same process should occur for each .xls file in the directory.  If one of the files does not pass
    validation then the job should be aborted and the error message presented to the user for correction. You will
    probably want to investigate the os module that comes standard with python for manipulating files in order to write
    this function.
    """

    if os.path.isfile(filename):
        model = PhyModel(filename)
        model.validate_model()
        if model.validation_message == '':
                model.create_ddl_file
        else: sys.exit(1)
    elif os.path.isdir(filename):
        for spreadsheet in os.listdir(filename):
            if spreadsheet.endswith(".xls"):
                model = PhyModel(spreadsheet)
                model.validate_model()
                if model.validation_message == '':
                    model.create_ddl_file
                else: sys.exit(1)
                continue
    else: sys.exit(1)


def teardown():
    """
    This is a placeholder for any cleanup work that may need to be done after the script is run. I am not sure if we will
    need this, but it is here as part of a general pattern I like to follow with a setup, main, and teardown structure for
    the python executable.
    """
    print "teardown"

if __name__ == "__main__":
   filename = setup(sys.argv)
   main(filename)
   teardown()