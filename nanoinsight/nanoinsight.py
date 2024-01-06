#!/usr/bin/env python3

import os
import nanoinsight

def annotate_ins(vcf, 
                 wk_dir, 
                 species, 
                 threads, 
                 mafft_exe=None,
                 repmask_exe=None,
                 ins_seq='ins_seq.fa', 
                 sv_sup='sv_support_reads.tsv'
                 ):
    # nanoinsight.check_args(species)
    # mafft_exe = nanoinsight.check_exe(mafft_exe, 'mafft')
    # repmask_exe = nanoinsight.check_exe(repmask_exe, 'RepeatMasker')
    print('Creating insertion fasta')
    id_seq, fasta_dir = nanoinsight.create_fa(vcf, wk_dir, sv_sup, ins_seq)
    print('Generating insertion sequence consensus')
    con_fasta, threads_per_job = nanoinsight.create_cons(vcf, wk_dir, fasta_dir, id_seq, threads, mafft_exe, batch_size=100, num_parallel_workers=5)
    print('Annotating insertions with RepeatMasker')
    nanoinsight.rep_annote(wk_dir, con_fasta, threads_per_job, species, repmask_exe)
    print('Finished')

def main():
    args = nanoinsight.get_args()
    # Observe verbosity
    if args.quiet:
        sys.stdout = open(os.devnull, 'w')
    os.makedirs(args.dir, exist_ok=True)
    annotate_ins(args.vcf, args.dir, args.species, args.threads, mafft_exe=args.mafftpath, repmask_exe=args.repmaskpath, ins_seq=args.insfa, sv_sup=args.suptsv)

if __name__ == "__main__":
    main()
