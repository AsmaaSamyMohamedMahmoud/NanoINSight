# INSight 
INSight is a repeat annotation tool for insertions called by [NanoVar](https://github.com/benoukraflab/nanovar).

## Installation:
```
git clone https://github.com/benoukraflab/INSight.git
cd INSight 
pip install .
```
## Installation of dependencies
### 1. _MAFFT_
#### Option 1: Conda 
```
 conda install -c bioconda mafft
 ```
#### Option 2: 
Please visit [here](https://mafft.cbrc.jp/alignment/software/source.html) to download the "without_extensions" source package 
and visit [here](https://mafft.cbrc.jp/alignment/software/installation_without_root.html) for instructions to install.
* Please note that MAFFT source package with extnesions is not needed as it supports RNA structural alignments. 
* Path of executable binary is needed. You can get it by typing "which mafft" in the terminal window. 
### 2. _RepeatMasker_
#### Option 1: Conda 
```
 conda install -c bioconda repeatmasker
```
#### Option 2: 
Please visit [here](https://www.repeatmasker.org/RepeatMasker/) for instructions to install.

## Run:
### Option 1: Run with NanoVar command by adding " " parameter 
```
nanovar [Options] "ins" sample.fq/sample.bam ref.fa working_dir 
```
For more details: see [NanoVar wiki](https://github.com/cytham/nanovar/wiki)

### Option 2: Run via the command-line 
```
INSight [-h] [-v] [-q] [-t int] [-i path] [-u path] [-m path] [-r path] 
        [-s species] [VCF] [working_directory]

Example:
        INSight -t 4 -s human sample.nanovar.pass.vcf ./work_dir
```
Required parameters:
| Parameter | Description |
| ------ | ------ |
| -s | Specify species for repeatmasker (e.g. human)|
| [VCF] | Path to VCF input file |
| [working_directory] | Path to working directory |

Additional Parameters:
| Parameter | Description |
| ------ | ------ |
| -h | Show help message |
| -v | Show version |
| -q | hide verbose |
| -t | Number of threads to be used [1]|
| -i | Path to ins_seq.fa file (NanoVar output) |
| -u | Path to sv_support_reads.tsv file (NanoVar output) |
| -m | Path to mafft executable file |
| -r | Path to RepeatMasker executable file |

## Output:
| Output | Description |
| ------ | ------ |
| .ins.con.fasta| fasta file of consensus sequences of insertions found in the VCF input file |
| rm_output | output directory of [RepeatMasker](https://www.repeatmasker.org/webrepeatmaskerhelp.html#reading) |

## Citation:
If you use INSight, please cite:

## Authors:
* **Asmaa Samy** - [AsmaaSamyMohamedMahmoud](https://github.com/AsmaaSamyMohamedMahmoud).
* **Tham Cheng Yong** - [cytham](https://github.com/cytham).
* **Touati Benoukraf** - [benoukraflab](https://github.com/benoukraflab).
