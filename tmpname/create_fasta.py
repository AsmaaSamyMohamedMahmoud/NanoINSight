import os
import allel
import pandas as pd

################################################################################################################################################################
#(1)Create fasta files of each INS
################################################################################################################################################################

def create_fa(vcf, wk_dir, sv_sup, ins_seq):
    sr = parse_vcf(vcf, wk_dir, sv_sup)
    id, seq = get_ins_seq(ins_seq)
    id_seq = match_reads(sr, id, seq)
    generate_fasta(id_seq, wk_dir)
    
## Parse VCF and supporting reads into dataframe
def parse_vcf(vcf, wk_dir, sv_sup):
    #Read vcf file to a df
    nanovar = allel.vcf_to_dataframe(vcf,fields=['ID','SVTYPE','CHROM', 'POS','SVLEN'])
    ##Extract only insertions
    ins = nanovar[nanovar['SVTYPE'] == 'INS'] 
    #Read supporting reads tsv file
    sr = pd.read_csv(sv_sup, sep = '\t')
    #Get SRs of INS only
    sr = pd.merge(ins, sr, how = 'inner', left_on = 'ID', right_on='SV-ID')
    sr.rename(columns = {'Supporting_reads (readname~index1,readname~index2...)':'id'}, inplace = True)
    #Split the comma-separated read_id values into separate rows
    sr['id'] = sr['id'].str.split(',')
    #Each row containing one read_id
    sr = sr.explode('id')
    return sr

## Get read ID and sequence from ins_seq.fa
def get_ins_seq(ins_seq):
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
    return id, seq

## Match reads with SV_IDs
def match_reads(sr, id, seq):
    #Formulate read id in a way to match with read IDs from tsv file and inner join with info of sr df 
    id= pd.DataFrame(id,columns = ['id'])
    id[["id", "coo"]] = id['id'].str.split("::", expand=True)
    seq= pd.DataFrame(seq,columns = ['seq'])
    id_seq = pd.concat([id, seq], axis = 1)
    id_seq= pd.merge(id_seq, sr, how="inner", on=['id'])
    #Add '>' as it is needed for alignment
    id_seq['coo']='>'+id_seq['coo'] 
    #Calculate end position and join all to add it later to con file header
    id_seq['end']=id_seq['POS']+id_seq['SVLEN']  ##### Why is chromosomal end coordinated calculated this way? Shouldn't 'end' be just POS+1? The length of the insert (SVLEN) should not be used to determine end coordinates, or am I reading this wrongly?
    id_seq['POS']=id_seq['POS'].astype(str)
    id_seq['end']=id_seq['end'].astype(str)
    id_seq['sv_coo']='::'+id_seq['CHROM']+':'+id_seq['POS']+'-'+id_seq['end']
    return id_seq

## Generate fasta file for each ins containing ins seqeunces from all SRs
def generate_fasta(id_seq, wk_dir):
    #Group seq and coordinates by SV-ID
    grouped = id_seq.groupby('ID')
    #Create the 'fasta_files' directory if it doesn't exist
    if not os.path.exists(os.path.join(wk_dir, 'fasta_files')):
        os.makedirs(os.path.join(wk_dir, 'fasta_files'))
    #Loop through each group and write it to a separate text file
    for sv_id, group_df in grouped:
        #Check the number of rows in group_df
        num_rows = group_df.shape[0]
        #Skip writing a fasta file for INS if there is only one SR 
        if num_rows > 1:
            filename = os.path.join(wk_dir, f'fasta_files/{sv_id}.fasta')
            output_str = group_df.iloc[:, [1, 2]].astype(str).agg('\n'.join, axis=1)
            #Write the content to the fasta file
            with open(filename, 'w') as f:
                f.write('\n'.join(output_str.tolist()))  # Join all rows and write them
