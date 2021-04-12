#!/usr/bin/python
# -*- coding: utf-8 -*-
# config.py

"""
This program store a series of fixed data and directory path,
also includes some print functions for error event happen
"""

# pylint: disable=C0116
# pylint: disable=C0103

# Dataset directory and data file type
_UNIGENE_DIR = '/data/PROGRAMMING/assignment5'
_UNIGENE_FILE_ENDING = 'unigene'

# Scientfic name
BOS_TARUS = 'Bos_taurus'
HOMO_SAPIENS = 'Homo_sapiens'
EQUUS_CABALLUS = 'Equus_caballus'
MUS_MUSCULUS = 'Mus_musculus'
OVIS_ARIES = 'Ovis_aries'
RATTUS_NORVEGICUS = 'Rattus_norvegicus'

# Map host keywords to scientfic name

HOST_KEYWORDS = {
    'bos taurus': BOS_TARUS,
    'cow': BOS_TARUS,
    'cows': BOS_TARUS,
    'homo sapiens': HOMO_SAPIENS,
    'human': HOMO_SAPIENS,
    'humans': HOMO_SAPIENS,
    'equus caballus': EQUUS_CABALLUS,
    'horse': EQUUS_CABALLUS,
    'horses': EQUUS_CABALLUS,
    'mouse': MUS_MUSCULUS,
    'mice': MUS_MUSCULUS,
    'mus musculus': MUS_MUSCULUS,
    'rat': RATTUS_NORVEGICUS,
    'rats': RATTUS_NORVEGICUS,
    'rattus norvegicus': RATTUS_NORVEGICUS,
    'sheep': OVIS_ARIES,
    'ovis aries': OVIS_ARIES,
}


def get_error_string_4_IOError(file=None, mode=None):
    """ Print the invalid argument type message and exits the program """

    print(f"Could not open the file: {file} for mode '{mode}'")


def get_error_string_4_ValueError():
    """ Print the invalid argument type message and exits the program """

    print('Invalid argument Value for opening a file for reading/writing')


def get_error_string_4_TypeError():
    """ Print the invalid argument type message and exits the program """

    print('Invalid argument Type passed in:')


def get_error_string_4_not_found_gene_for_host(host, gene):
    """ Print the invalid argument type message and exits the program """

    print('Not found')
    print(f'Gene {gene} does not exist for {host}. exiting now...')


def get_error_string_4_not_found_host():
    """ Print the help msg when input host is not exist """

    print('Either the Host Name you are searching for is not in the database\n')
    print('or If you are trying to use the scientific\
    name please put the name in double quotes:\n')
    print('"Scientific name"\n')


def get_unigene_directory():
    """ Get unigene directory """

    return _UNIGENE_DIR


def get_unigene_extension():
    """ Get unigene file extension """

    return _UNIGENE_FILE_ENDING


def get_host_keyword():
    """ Get host keywords map rules """

    return HOST_KEYWORDS
