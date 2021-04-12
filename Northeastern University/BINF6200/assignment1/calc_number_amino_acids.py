#!/usr/bin/env python3
# calc_number_amino_acids.py
"""use input number to calculate the number of amino acids and the estimate molecular weight."""
# Set DNA sequence name and its length as inputs.
SEQ_NAME = input('Please enter a name for the DNA sequence: ')
print('Your sequence name is: {}'.format(SEQ_NAME))

SEQ_LEN = int(input('Please enter the length of the sequence: '))
if SEQ_LEN % 3 == 0:
    print('The length of DNA sequence is: {}'.format(SEQ_LEN))
    PROTEIN_NUM = SEQ_LEN/3
    AVERAGE_WEIGHT = (PROTEIN_NUM * 110)/1000
    print('The length of decoded protein is: {}'.format(PROTEIN_NUM))
    print('The average weight of the protein sequence is: {}'.format(AVERAGE_WEIGHT))
else:
    print('Error: the DNA sequence is not a multiple of 3')
