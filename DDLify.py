import sys, getopt
from DDLify.utility_funcs import print_usage

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "hd:f:", ["directory=", "filename="])
    except getopt.GetoptError:
        print_usage()


if __name__ == "__main__":
   main(sys.argv[1:])