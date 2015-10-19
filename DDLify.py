import sys
from DDLify.utility_funcs import print_usage

def setup(argv):
    if len(argv) != 2:
        print_usage()
        sys.exit(2)
    else:
        filename = argv[1]

    return filename



def main(filename):
    print "To-Do"


def teardown():
    print "teardown"

if __name__ == "__main__":
   filename = setup(sys.argv)
   main(filename)
   teardown()