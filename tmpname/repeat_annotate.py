import os
import subprocess

################################################################################################################################################################
#(3) Annotation using RepeatMasker 
################################################################################################################################################################    

def rep_annote(wk_dir, samplename, threads_per_job, species):
    input_sequence = os.path.join(wk_dir, f"{samplename}.ins.con.fasta")
    rm_dir = os.path.join(wk_dir, "rm_output")
    if not os.path.exists(rm_dir):
          os.makedirs(rm_dir)
    # species = species
    subprocess.run([f"RepeatMasker -species {species} -s -pa {threads_per_job} {input_sequence} -dir {rm_dir}"],
                   capture_output=True, text=True, shell = True)
    # return {input_dir, MA_dir, con_dir, f"{samplename}.ins.con.fasta", RM_dir}
