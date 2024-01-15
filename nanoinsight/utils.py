import os
import sys
import argparse
import distutils.spawn
from nanoinsight import __version__

# Parse input arguments
def get_args(args=sys.argv[1:]):

    parser = argparse.ArgumentParser(description="NanoINSight is a repeat annotation tool for insertions called by NanoVar",
                                     formatter_class=argparse.RawTextHelpFormatter, usage=msg(), add_help=False)

    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    required.add_argument("-s", "--species", type=str, metavar="str",
                          help="specify species for repeatmasker (e.g. human)", required=True)
    
    required.add_argument("vcf", type=str,
                          metavar="[VCF]",
                          help="path to input VCF file")

    required.add_argument("dir", type=str,
                          metavar="[work_directory]",
                          help="path to work directory")

    optional.add_argument("-h", "--help", action="help",
                          default=argparse.SUPPRESS,
                          help="show this help message and exit")
    
    optional.add_argument("-i", "--insfa", type=str, metavar="path",
                        help="""specify path to ins_seq.fa file from NanoVar, 
otherwise assumed in work directory""")

    optional.add_argument("-u", "--suptsv", type=str, metavar="path",
                        help="""specify path to sv_support_reads.tsv file from NanoVar, 
otherwise assumed in work directory""")
    
    optional.add_argument("-m", "--mafftpath", type=str, metavar="path",
                        help="specify path to 'mafft' executable")

    optional.add_argument("-r", "--repmaskpath", type=str, metavar="path",
                        help="specify path to 'RepeatMasker' executable")
    
    def restrict_threads(t):
        t = int(t)
        if t < 1:
            raise argparse.ArgumentTypeError("Number of threads specified < 1, minimum requirement is 1 thread.")
        return t
    
    optional.add_argument("-t", "--threads", type=restrict_threads, metavar="int",
                        default=1,
                        help="specify number of threads [1]")

    optional.add_argument("-v", "--version", action='version',
                        version=__version__,
                        help="print version")
    
    optional.add_argument("-q", "--quiet", action='store_true',
                        help="hide verbose")
  
    args = parser.parse_args(args)
    
    check_args(args.species)
    args.mafftpath = check_exe(args.mafftpath, 'mafft')
    args.repmaskpath = check_exe(args.repmaskpath, 'RepeatMasker')
    args.insfa, args.suptsv = check_files(args.insfa, args.suptsv, args.dir)
    return args

# Custom usage message
def msg():
    return "nanoinsight [options] -s [species] [VCF] [work_directory]"

# Check args
def check_args(species):
    # Check mandatory args
    common_species = ['human', 'mouse', 'rattus']
    if species is None:
        raise Exception("Error: Repeatmasker species is not provided, please specify %s." % ', '.join(common_species))
    elif species not in common_species:
        raise Exception("Error: %s species is not supported, please use %s, or contact us on GitHub" % (species, ', '.join(common_species))) 

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

# Check file paths
def check_files(insfa, suptsv, wk_dir):
    if insfa is None:
        insfa = os.path.join(wk_dir, 'ins_seq.fa')
    if suptsv is None:
        suptsv = os.path.join(wk_dir, 'sv_support_reads.tsv')
    if not os.path.isfile(insfa):
        raise Exception("Error: ins_seq.fa file is not found in %s." % insfa)  
    if not os.path.isfile(suptsv):
        raise Exception("Error: sv_support_reads.tsv file is not found in %s." % suptsv)
    return insfa, suptsv
