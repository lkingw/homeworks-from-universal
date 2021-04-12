#!/usr/bin/env python3
# pdb_fasta_splitter.py
"""
We wrote this program to generate two files. One with the
protein seq and the other one with secondary structures.
Then, we count the numbers of the protein seq and secondary
structures
"""

import sys
import argparse


def main():
    """Business Logic"""
    args = get_cli_args()
    infile, mode = args.infile, 'r'
    fh_in = get_fh(infile, mode)
    pdb_protein_fh = get_fh('pdb_protein.fasta', 'w')
    pdb_ss_fh = get_fh('pdb_ss.fasta', 'w')
    list_headers, list_seqs = get_header_and_sequence_lists(fh_in)
    seq_count, ss_count = 0, 0
    for i, header in enumerate(list_headers):
        if header.endswith('sequence'):
            pdb_protein_fh.write(header+'\n')
            pdb_protein_fh.write(list_seqs[i]+'\n')
            seq_count += 1
        elif header.endswith('secstr'):
            pdb_ss_fh.write(header+'\n')
            pdb_ss_fh.write(list_seqs[i]+'\n')
            ss_count += 1
    print('Found {} protein sequences'.format(seq_count))
    print('Found {} ss sequences'.format(ss_count))
    pdb_protein_fh.close()
    pdb_ss_fh.close()

# define a function to get file handle to sequences
# in fasta file and open two outfiles


def get_fh(infile, mode):
    """get the file handle"""
    try:
        file_handle = open(infile, mode=mode)
        return file_handle
    except IOError as error:
        print('cannot open', infile)
        raise error
    except ValueError as error:
        print('wrong open mode')
        raise error

# Define a function to get sequence and header that
# one-to-one correspondence to the data in the lists


def get_header_and_sequence_lists(fh_in):
    """Return header list and sequence list"""
    list_headers = []
    list_seqs = []
    lines = fh_in.readlines()
    for idx, line in enumerate(lines):
        # use .rstrip to get rid of the empty space and \n at the end of str
        line = line.rstrip()
        if line.startswith('>'):
            header_line = line
            list_headers.append(header_line)
            s_idx = idx + 1
            sequence = ''
            while s_idx < len(lines) and not lines[s_idx].startswith('>'):
                # use .replace to only get rid of the \n at the end of str
                sequence += lines[s_idx].replace("\n", "")
                s_idx += 1
            if sequence != '':
                list_seqs.append(sequence)
            else:
                continue
    if _check_size_of_lists(list_headers, list_seqs):
        # print(list_headers)
        # print(list_seqs)
        return list_headers, list_seqs

# define a internal used function to check if the size of
# header list and sequence list are equal.


def _check_size_of_lists(list_headers, list_seqs):
    """check if the size of header list and seq list are equal """
    if len(list_headers) != len(list_seqs):
        sys.exit("The size of the sequences and the header lists is different \n"
                 "Are you sure the FASTA is in correct format")
    else:
        return True


def get_cli_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """
    parser = argparse.ArgumentParser(
        description='Give the fasta sequence file name to do the splitting')
    parser.add_argument('-i', '--infile', dest='infile',
                        type=str, help='Path to the file to open',
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
    main()
