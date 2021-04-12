#!/usr/bin/env python3
# calc_daltons.py
"""calculates the estimated molecular weight of the protein and writes the result on the screen"""
# Set the value of the amino acids and the molecular weight per amino acid.
AMINO_NUM = 671
AVE_MOLE_WEIGHT = 110
AVE_PRO_WEIGHT = (AMINO_NUM * AVE_MOLE_WEIGHT)/1000
print('The length of "Protein kinase C beta type" is : {}'.format(AMINO_NUM))
print('The average weight of this protein sequence in kilodaltons is: {}'.format(AVE_PRO_WEIGHT))
