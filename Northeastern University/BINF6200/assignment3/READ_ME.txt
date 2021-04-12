## Overview

In this assignment, we defined a function to take input file and pass back a file project. We got file handle and ruturn header and seq list of the fasta file, and we check the size of them.
We also defined functions to count the occurrence of the nucleotides, gc content and get the accession number from each header string. 

## Author

Xindi Chen

## Date Created

3/1/2021

## run the excutable scripts

python3 pdb_fasta_splitter.py --infile ss.txt
python3 pdb_fasta_splitter.py -h
python3 pdb_fasta_splitter.py
python3 pdb_fasta_splitter.py --infile ss_designed2Fail.txt

python3 nucleotide_statistics_from_fasta.py --infile influenza.fasta --outfile influenza.stats.txt
python3 nucleotide_statistics_from_fasta.py -h
python3 nucleotide_statistics_from_fasta.py
python3 nucleotide_statistics_from_fasta.py --infile influenza.fasta