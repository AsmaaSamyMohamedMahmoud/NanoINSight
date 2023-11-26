import sys
import argparse
import distutils.spawn
from tmpname import __version__

# Parse input arguments
def get_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="tmpname tool description",
                                     formatter_class=argparse.RawTextHelpFormatter, usage=msg())

    parser.add_argument("vcf", type=str,
                        metavar="[VCF]",
                        help="path to input VCF file")

    parser.add_argument("dir", type=str,
                        metavar="[work_directory]",
                        help="path to work directory")
  
    parser.add_argument("-s", "--species", type=str, metavar="str",
                        help="specify species for repeatmasker (e.g. human)")

    parser.add_argument("-i", "--insfa", type=str, metavar="path",
                        help="""specify path to ins_seq.fa file from NanoVar, 
otherwise assumed in work directory""")

    parser.add_argument("-u", "--suptsv", type=str, metavar="path",
                        help="""specify path to sv_support_reads.tsv file from NanoVar, 
otherwise assumed in work directory""")
    
    parser.add_argument("-m", "--mafftpath", type=str, metavar="path",
                        help="specify path to 'mafft' executable")
    
    def restrict_threads(t):
        if t < 1:
            raise argparse.ArgumentTypeError("Number of threads specified < 1, minimum requirement is 1 thread.")
        return t
    
    parser.add_argument("-t", "--threads", type=restrict_threads, metavar="int",
                        default=1,
                        help="specify number of threads [1]")

    parser.add_argument("-v", "--version", action='version',
                        version=__version__,
                        help="prints version")
  
    args = parser.parse_args(args)
    
    check_args(args.species)
    args.mafftpath = check_exe(args.mafftpath, 'mafft')
    return args

# Custom usage message
def msg():
    return "tmpname [options] -s [species] [VCF] [work_directory]"

# Check args
def check_args(species, mafft_exe):
    # Check mandatory args
    common_species = ['human', 'mouse', 'rattus']
    if species is None:
        raise Exception("Error: Repeatmasker species is not provided, please specify %s." % ', '.join(common_species))
    elif species not in common_species:
        raise Exception("Error: %s species is not supported, please use %s, or contact us on GitHub" % (args.species, ', '.join(common_species))) 

# Check paths and executables
def check_exe(path, exe):
    if path is None:
        if distutils.spawn.find_executable(exe):
            return exe
        else:
            raise Exception("Error: %s executable is not in PATH" % exe)
    else:
        if distutils.spawn.find_executable(path):
            return path
        else:
            raise Exception("Error: %s path do not exist" % path)
    
