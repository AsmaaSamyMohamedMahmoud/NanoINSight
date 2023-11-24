import sys
import argparse
from tmpname import __version__

# Parse input arguments
def get_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="tmpname tool description",
                                     formatter_class=argparse.RawTextHelpFormatter, usage=msg())

    parser.add_argument("input", type=str,
                        metavar="[VCF]",
                        help="path to input VCF file")

    parser.add_argument("dir", type=str,
                        metavar="[work_directory]",
                        help="path to work directory")
  
    parser.add_argument("-s", "--species", type=str, metavar="str",
                        help="specify species for repeatmasker (e.g. human)")

    parser.add_argument("-i", "--ins-fa", type=str, metavar="path",
                        help="""specify path to ins_seq.fa file from NanoVar, 
otherwise assumed in work directory""")

    parser.add_argument("-u", "--sup-tsv", type=str, metavar="path",
                        help="""specify path to sv_support_reads.tsv file from NanoVar, 
otherwise assumed in work directory""")
    
    parser.add_argument("--mafft-path", type=str, metavar="path",
                        help="specify path to 'mafft' executable")

    parser.add_argument("-t", "--threads", type=int, metavar="int",
                        default=1,
                        help="specify number of threads [1]")

    parser.add_argument("-v", "--version", action='version',
                        version=__version__,
                        help="prints version")
  
    args = parser.parse_args(args)
    return args

# Custom usage message
def msg():
    return "tmpname [options] -s [species] [VCF] [work_directory]"
