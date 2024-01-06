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
    p = subprocess.run([f"RepeatMasker -species {species} -s -pa {threads_per_job} {con_fasta} -dir {rm_dir} -e rmblast"],
                   capture_output=True, text=True, shell=True)
    if p.returncode != 0:
        err = p.stderr.strip()
        raise Exception('RepeatMasker returned non-zero exit status:\n %s' % err)
    # return {input_dir, MA_dir, con_dir, f"{samplename}.ins.con.fasta", RM_dir}
