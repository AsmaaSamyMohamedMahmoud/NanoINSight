import os
import subprocess

################################################################################################################################################################
#(3) Annotation using RepeatMasker 
################################################################################################################################################################    

def rep_annote(wk_dir, con_fasta, threads_per_job, species):
    # input_sequence = os.path.join(wk_dir, f"{samplename}.ins.con.fasta")
    rm_dir = os.path.join(wk_dir, "rm_output")
    os.makedirs(rm_dir, exist_ok=True)
    # species = species
    subprocess.run([f"RepeatMasker -species {species} -s -pa {threads_per_job} {con_fasta} -dir {rm_dir}"],
                   capture_output=True, text=True, shell=True, check=True)
    # return {input_dir, MA_dir, con_dir, f"{samplename}.ins.con.fasta", RM_dir}
