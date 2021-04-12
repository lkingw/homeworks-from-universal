#!/usr/bin/env python3
# nucleotide_statistics_from_fasta.py
"""
Similar to the first program, but get stats from each seq and header string
"""

import sys
# import os
# import re
import argparse


def main():
    """Business Logic"""
    args = get_cli_args()
    infile, read_mode = args.infile, 'r'
    outfile, write_mode = args.outfile, 'w'
    fh_in = get_fh(infile, read_mode)
    fh_out = get_fh(outfile, write_mode)
    list_headers, list_seqs = get_header_and_sequence_lists(fh_in)
    print_sequence_stats(list_headers, list_seqs, fh_out)
    fh_out.close()

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
        line = line.rstrip()
        if line.startswith('>'):
            header_line = line
            list_headers.append(header_line)
            s_idx = idx + 1
            sequence = ''
            while s_idx < len(lines) and not lines[s_idx].startswith('>'):
                sequence += lines[s_idx].rstrip()
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
    """check if the size of header list and seq list are equal"""
    if len(list_headers) != len(list_seqs):
        sys.exit("The size of the sequences and the header lists is different \n"
                 "Are you sure the FASTA is in correct format")
    else:
        return True


def print_sequence_stats(list_headers, list_seqs, fh_out):
    """print the stats of the number of nucleotide, seq length and gc countent"""
    fh_out.write("Number\tAccession\tA's\tG's\tC's\tT's\tN's\tLength\tGC%\n")
    num = 0
    for index, seq in enumerate(list_seqs):
        num += 1
        accession_num = _get_accession(list_headers[index])
        num_as = _get_nt_occurrence('A', seq)
        num_gs = _get_nt_occurrence('G', seq)
        num_cs = _get_nt_occurrence('C', seq)
        num_ts = _get_nt_occurrence('T', seq)
        num_ns = _get_nt_occurrence('N', seq)
        gc_count = num_gs + num_cs
        gc_countent = (gc_count/len(seq))*100
        length = len(seq)
        # write out the outfile and print the result in format
        fh_out.write(f"{num}\t{accession_num}\t{num_as}\t{num_gs}\t"
                     f"{num_cs}\t{num_ts}\t{num_ns}\t{length}\t{gc_countent:.1f}\n")


def _get_nt_occurrence(nucleotide, seq):
    """count the number of nucleotides"""
    if nucleotide in ['A', 'C', 'G', 'T', 'N']:
        return seq.count(nucleotide)
    sys.exit("Did not code this condition")


def _get_accession(header_string):
    """get the accession number of the header string"""
    # Use the .split to split the header string and keep the first element
    line = header_string
    word = line.split()[0]
    # get the accession number after the ">"
    a_c = word.split('>')[1]
    return a_c


def get_cli_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """
    parser = argparse.ArgumentParser(
        description='Give the fasta sequence file name to get the nucleotide statistics')
    parser.add_argument('-i', '--infile', dest='infile',
                        type=str, help='Path to the file to open', required=True)
    parser.add_argument('-o', '--outfile', dest='outfile',
                        type=str, help='Path to the file to write', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    main()
