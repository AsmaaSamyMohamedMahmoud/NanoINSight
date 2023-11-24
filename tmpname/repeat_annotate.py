import os

################################################################################################################################################################
#(3) Annotation using RepeatMasker 
################################################################################################################################################################    

def rep_annote(wk_dir, samplename, threads_per_job, species):
    input_sequence = os.path.join(wk_dir, f"{samplename}.ins.con.fasta")
    RM_dir = os.path.join(wk_dir, "RM_output")
    # species = species
    subprocess.run([f"RepeatMasker -species {species} -s -pa {threads_per_job} {input_sequence} -dir {RM_dir}"]
                   , capture_output=True,text=True, shell = True)
    # return {input_dir, MA_dir, con_dir, f"{samplename}.ins.con.fasta", RM_dir}
