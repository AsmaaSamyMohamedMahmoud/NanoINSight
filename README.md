# Annotation-of-insertions
### Installation of dependencies
* python package "scikit-allel"
* Biopython >=v1.79
* RepeatMasker
##### 1. _scikit-allel_
#### Option 1: Conda 
```
conda install -c conda-forge scikit-allel
```
#### Option 2: PyPI 
```
pip install scikit-allel[full]
```
##### 2. _Biopython_
#### using PyPI
```
pip install biopython
*make sure the version is >=1.79 
```
##### 2. _RepeatMasker_
#### Option 1: Conda 
```
 conda install -c bioconda repeatmasker
```
#### Option 2: 
```
Please visit [here](https://www.repeatmasker.org/RepeatMasker/)https://www.repeatmasker.org/RepeatMasker/) for instructions to install.
```
* Please note that this script will utilize 75% of the available CPUs for multiple alignment using MAFFT.
