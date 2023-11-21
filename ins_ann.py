#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:09:41 2023

@author: asmaa
"""

import os
import re
import allel
import pandas as pd
import psutil
from concurrent.futures import ThreadPoolExecutor
from Bio import AlignIO
from Bio.Align import AlignInfo
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
import subprocess

################################################################################################################################################################
#(1)Create fasta files of each INS
################################################################################################################################################################
#Same path of the work directory of nanovar
def INS_ANN(input_dir, mafft_exe, species):
    os.chdir(input_dir)
    vcf_file = [file for file in os.listdir() if re.match(r'.*\.vcf$', file)]
    ##to make vcf variable as a string 
    vcf = vcf_file[0]
#Read vcf file to a df
    nanovar = allel.vcf_to_dataframe(vcf,fields=['ID','SVTYPE','CHROM', 'POS','SVLEN'])
##Extract only insertions
    ins = nanovar[nanovar['SVTYPE'] == 'INS'] 
#Read supporting reads tsv file
    sr = pd.read_csv('sv_support_reads.tsv', sep = '\t')
#Get SRs of INS only
    sr = pd.merge(ins, sr, how = 'inner', left_on = 'ID', right_on='SV-ID')
    sr.rename(columns = {'Supporting_reads (readname~index1,readname~index2...)':'id'}, inplace = True)
#Split the comma-separated read_id values into separate rows
    sr['id'] = sr['id'].str.split(',')
#Each row containing one read_id
    sr = sr.explode('id')

##Get read id and sequence from the ins_seq.fa to match reads with SV_IDs
    id = []
    seq = []
    with open('ins_seq.fa') as f:
        read = f.readlines()
    for i in range(len(read)):
        read[i]=read[i].rstrip()
        if read[i].startswith('>'):
            read[i]=read[i].lstrip('>')
            id.append(read[i])
        else:
            seq.append(read[i])
    f.close()

#Formulate read id in a way to match with read IDs from tsv file and inner join with info of sr df 
    id= pd.DataFrame(id,columns = ['id'])
    id[["id", "coo"]] = id['id'].str.split("::", expand=True)
    seq= pd.DataFrame(seq,columns = ['seq'])
    id_seq = pd.concat([id, seq], axis = 1)
    id_seq= pd.merge(id_seq, sr, how="inner", on=['id'])

#Add '>' as it is needed for alignment
    id_seq['coo']='>'+id_seq['coo'] 
#Calculate end position and join all to add it later to con file header
    id_seq['end']=id_seq['POS']+id_seq['SVLEN']
    id_seq['POS']=id_seq['POS'].astype(str)
    id_seq['end']=id_seq['end'].astype(str)
    id_seq['sv_coo']='::'+id_seq['CHROM']+':'+id_seq['POS']+'-'+id_seq['end']

##Generate fasta file for each ins containing ins seqeunces from all SRs 
#Group seq and coordinates by SV-ID
    grouped = id_seq.groupby('ID')
#Create the 'fasta_files' directory if it doesn't exist
    if not os.path.exists('fasta_files'):
        os.makedirs('fasta_files')
#Loop through each group and write it to a separate text file
    for sv_id, group_df in grouped:
    #Check the number of rows in group_df
        num_rows = group_df.shape[0]
    #Skip writing a fasta file for INS if there is only one SR 
        if num_rows > 1:
            filename = f'fasta_files/{sv_id}.fasta'
            output_str = group_df.iloc[:, [1, 2]].astype(str).agg('\n'.join, axis=1)
        #Write the content to the fasta file
            with open(filename, 'w') as f:
                f.write('\n'.join(output_str.tolist()))  # Join all rows and write them
            
################################################################################################################################################################
#(2) Generating multiple alignment and consensus sequences for each INS
################################################################################################################################################################              
# Get the total number of CPU threads
    total_cpus = os.cpu_count()
# Calculate the available CPU threads based on CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)  # Adjust the interval as needed
    available_cpus = total_cpus * (1 - (cpu_usage / 100))
# Calculate num_threads as 75% of the available CPUs
    num_threads = int(available_cpus * 0.75)
# Ensure the number of threads is at least 1
    num_threads = max(num_threads, 1)
    #print ('No of threads is used for Mafft is', num_threads)
# Define your batch size and number of parallel workers
    batch_size = 100
    num_parallel_workers = 5  # You want to process 5 batches concurrently
    threads_per_job=int(num_threads/num_parallel_workers)
    #print ('No of threads for each job is', threads_per_job)
    input_dir = "./fasta_files"
    MA_dir = "./MA"
    con_dir = "./con"
    mafft_exe = mafft_exe #input arg
    os.makedirs(MA_dir, exist_ok=True)
    os.makedirs(con_dir, exist_ok=True)

    def process_batch(batch):
        for input_file in batch:
            if input_file.endswith(".fasta"):
            # Input and output file paths
                input_path = os.path.join(input_dir, input_file)
                MA_file = os.path.join(MA_dir, input_file.replace(".fasta", ".MA.fasta"))
                con_file = os.path.join(con_dir, input_file.replace(".fasta", ".con.fasta"))

            # Run MAFFT with MafftCommandline
                mafft_cline = MafftCommandline(mafft_exe,input=input_path, auto=True, thread=threads_per_job)
                stdout, stderr = mafft_cline()
                with open(MA_file, "w") as out_file:
                    out_file.write(stdout)

            # Generate consensus sequence for the output file
                alignment = AlignIO.read(MA_file, "fasta")
                summary = AlignInfo.SummaryInfo(alignment)
                consensus = summary.dumb_consensus(threshold=0.51, ambiguous='X')

            # Write consensus sequence to output file
                consensus_record = SeqRecord(Seq(consensus), id="consensus")
                SeqIO.write(consensus_record, con_file, "fasta")

    files = [f for f in os.listdir(input_dir) if f.endswith(".fasta")]

    with ThreadPoolExecutor(max_workers=num_parallel_workers) as executor:
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            executor.submit(process_batch, batch)
    #print ('Generating consensus sequences is DONE')

##Header of each file should be renamed to the SV ID
    for con_file in os.listdir(con_dir):
        if con_file.endswith(".fasta"):
    #Split filename and extension
            name, ext = os.path.splitext(con_file)
        #Remove the '.con' extension from the name
            name = name.replace('.con', '')
       #Add coordinates of SV to the header line
            matching_row = id_seq[id_seq['ID'] == name]
            info_to_add = matching_row['sv_coo'].values[0]
        #Open file and read lines
            with open(os.path.join(con_dir, con_file), "r") as f:
                lines = f.readlines()
        # Replace first line with filename (without extension) and remove ".con.fasta" if it's there
            new_header = f">{name}{info_to_add}\n"
            lines[0] = new_header
        
        #Open file for writing and write updated lines
            with open(os.path.join(con_dir, con_file), "w") as f:
                f.writelines(lines)
    #print ('Renaming is DONE')

# Concatenate all consensus sequences in one file for RM
    samplename, ext = os.path.splitext(vcf)
    samplename = samplename.replace('.nanovar.pass', '')
    subprocess.run([f"cat {con_dir}/*.fasta > {samplename}.ins.con.fasta"], capture_output=True, text=True, shell = True)

################################################################################################################################################################
#(3) Annotation using RepeatMasker 
################################################################################################################################################################     
    input_sequence = "{samplename}.ins.con.fasta"
    RM_dir = "./RM_ouptut/"
    species = species
    subprocess.run([f"RepeatMasker -species {species} -s -pa {threads_per_job} {input_sequence} -dir {RM_dir}"]
                   , capture_output=True,text=True, shell = True)
    
    return {input_dir, MA_dir, con_dir,f"{samplename}.ins.con.fasta", RM_dir}
    
##Usage
#input_dir = '/home/asmaa/Desktop/MUN_PhD/PhD_research/NanoVar2/Ins_seq/test'
#mafft_exe = '/usr/bin/mafft'
#species = 'human'
#outputs = INS_ANN(input_dir, mafft_exe,species)


