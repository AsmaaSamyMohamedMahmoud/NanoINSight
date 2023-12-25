#!/usr/bin/env python3

import os
import INSight

def annotate_ins(vcf, 
                 wk_dir, 
                 species, 
                 threads, 
                 mafft_exe=None, 
                 ins_seq='ins_seq.fa', 
                 sv_sup='sv_support_reads.tsv'
                 ):
    INSight.check_args(species)
    mafft_exe = INSight.check_exe(mafft_exe, 'mafft')
    print('Creating insertion fasta')
    id_seq, fasta_dir = INSight.create_fa(vcf, wk_dir, sv_sup, ins_seq)
    print('Generating insertion sequence consensus')
    con_fasta, threads_per_job= INSight.create_cons(vcf, wk_dir, fasta_dir, id_seq, threads, mafft_exe, batch_size=100, num_parallel_workers=5)
    print('Annotating insertions with RepeatMasker')
    INSight.rep_annote(wk_dir, con_fasta, threads_per_job, species)
    print('Finished')

def main():
    args = INSight.get_args()
    # Observe verbosity
    if args.quiet:
        sys.stdout = open(os.devnull, 'w')
    os.makedirs(args.dir, exist_ok=True)
    annotate_ins(args.vcf, args.dir, args.species, args.threads, mafft_exe=args.mafftpath, ins_seq=args.insfa, sv_sup=args.suptsv)

if __name__ == "__main__":
    main()