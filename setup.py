from setuptools import setup, find_packages
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

exec(open("nanoinsight/version.py").read())

setup(
    name='NanoINSight',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/AsmaaSamyMohamedMahmoud/nanoinsight',
    license='gpl-3.0',
    author='Asmaa',
    author_email='asmmahmoud@mun.ca',
    description='Repeat annotation tool for insertions called by NanoVar',
    keywords=['insertion', 'structural variant','repeat annotation'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['biopython>=1.82', 'scikit-allel>=1.3.7', 'pandas>=1.5.3'],
    entry_points={
        "console_scripts": [
            "nanoinsight=nanoinsight.nanoinsight:main",
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
