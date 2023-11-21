# Annotation-of-insertions
### Installation of dependencies
* python package "scikit-allel"
* Biopython >=v1.79
* MAFFT
* RepeatMasker
##### 1. _scikit-allel_
##### Option 1: Conda 
```
conda install -c conda-forge scikit-allel
```
##### Option 2: PyPI 
```
pip install scikit-allel[full]
```
##### 2. _Biopython_
##### using PyPI
```
pip install biopython
```
* Please make sure the version is >=1.79 
##### 3. _MAFFT_
##### Option 1: Conda 
```
 conda install -c bioconda mafft
 ```
##### Option 2: 
Please visit [here] (https://mafft.cbrc.jp/alignment/software/source.html) to download the "without_extensionx" source package 
Please visit [here] (https://mafft.cbrc.jp/alignment/software/installation_without_root.html) for instructions to install.
* Please note that MAFFT source package with extnesions is not needed as it supports RNA structural alignments. 
* Path of executable binary is needed. You can get it by typing "which mafft" in your terminal window. 
##### 4. _RepeatMasker_
##### Option 1: Conda 
```
 conda install -c bioconda repeatmasker
```
##### Option 2: 
Please visit [here](https://www.repeatmasker.org/RepeatMasker/) for instructions to install.

* Please note that this script will utilize 75% of the available CPUs for multiple alignment using MAFFT.
