#!/usr/bin/python
# -*- coding: utf-8 -*-
# gene_information_query.py

"""
This program receive user input (host and gene) to access
corresponding file, and then print exsited tissue names in the file
"""

import re
import sys
import argparse
from assignment5 import my_io
from assignment5 import config


def print_tissues_data(tissues):
    """
    Print out the found tissues
    @param tissues: extracted tissue list without cleaning
    """
    cleaned_tissues = []

    # Clean the tissue data
    for tissue in tissues:
        if tissue[0] == ' ':
            tissue = tissue[1:]
        cleaned_tissues.append(tissue)

    # Sort list by alphabetical
    cleaned_tissues = sorted(cleaned_tissues, key=str.lower)
    for (i, tissue) in enumerate(cleaned_tissues):
        print('{:>3}'.format(i + 1) + '. ' + tissue[0].capitalize() + tissue[1:])


def get_gene_data(temp_host, gene):
    """
    Get gene data from dataset and then print it
    @param temp_host: host name from user input
    @param gene: gene name from user input
    """
    # Convert input host to scientific name if it is possible
    host = modify_host_name(temp_host)

    # Find the file path of gene data
    file_path = '/'.join((config.get_unigene_directory(), host, gene + '.' + config.get_unigene_extension()))

    # Check for the existence of file
    if my_io.is_valid_gene_file_name(file_path):

        print(f'\nFound Gene {gene} for {host}')
        file = my_io.get_fh(file_path, 'r')
        for line in file:
            if line.startswith('EXPRESS'):

                # extract the tissues-related string
                match = re.search('EXPRESS     (.*)', line)
                if match:
                    tissue_strig = match.group(1)

                    # split tissues
                    tissues = tissue_strig.split('|')
                    tissues_num = len(tissues)
                    print(f'In Homo sapiens, There are {tissues_num} tissues that TGM1 is expressed in:\n')
                    print_tissues_data(tissues)
                    break
    else:

        # If not, print error message and exit
        config.get_error_string_4_not_found_gene_for_host(host, gene)
        sys.exit()


def modify_host_name(temp_host):
    """
    Map input host to scientific name
    @param temp_host: host name from user input
    @return scientific name of the temp_host if it exsited
    """
    keywords = config.get_host_keyword()
    temp_host = temp_host.replace('_', ' ').lower()
    if temp_host in keywords:
        return keywords[temp_host]

    # If failure to convert, print exsited host list and exit
    _print_host_directories()
    sys.exit()


def _print_host_directories():
    """
    Print the exsited host in out dataset
    """
    config.get_error_string_4_not_found_host()
    print('Here is a (non-case sensitive)\
        list of available Hosts by scientific name\n')
    keywords = config.get_host_keyword()
    values = list(keywords.values())
    values = list(set(values))
    for (i, value) in enumerate(values):
        print('{:>3}'.format(i + 1) + '. ' + value)

    print('Here is a (non-case sensitive) \
        list of available Hosts by common name')
    keywords = config.get_host_keyword()
    for (i, word) in enumerate(keywords):
        print('{:>3}'.format(i + 1) + '. ' + word[0].capitalize() + word[1:])


def get_cli_args():
    """
    Get the command line options using argparse
    @return user input argument list
    """
    parser = \
        argparse.ArgumentParser(description='Give the Host and Gene name')

    parser.add_argument('-host', dest='host',
                        default='Homo sapiens', type=str,
                        help='Name of Host', required=False)

    parser.add_argument('-gene', dest='gene',
                        default='TGM1', type=str,
                        help='Name of Gene', required=False)

    return parser.parse_args()


def main():
    """
    Business Logic
    """
    args = get_cli_args()
    host = args.host
    gene = args.gene
    get_gene_data(host, gene)


if __name__ == '__main__':
    main()
