#!/usr/bin/python3

"""
Test suite for my_io.py
"""
import os
import pytest
from assignment4.my_io import get_fh

# pylint: disable=C0116
# pylint: disable=C0103

FILE_2_TEST = 'chr21_genes.txt'
FILE_LINES = \
    """
TPTE	tensin, putative protein-tyrosine phosphatase, EC 3.1.3.48.	1.1
CYC1LP4	cytochrome c pseudogene	5
Pseudo1	putative zinc finger protein pseudogene	5
PRED1	putative gene, protein kinase C ETA type (EC 2.7.1.) like	3.2
ORLP1	pheromone receptor pseudogene	5
"""


def test_existing_get_fh_4_reading():
    # does it open a file for reading
    # test
    test = get_fh(FILE_2_TEST, "r")
    assert hasattr(test, "readline") is True, "Not able to open for reading"


def test_existing_get_fh_4_writing():
    # does it open a file for writing
    # test
    test = get_fh('test.txt', mode="w")
    assert hasattr(test, "write") is True, "Not able to open for writing"
    test.close()
    os.remove('test.txt')


def test_get_fh_4_IOError():
    # does it raise IOError
    # this should exit
    with pytest.raises(IOError):
        get_fh("does_not_exist.txt", "r")


def test_get_fh_4_ValueError():
    # does it raise ValueError
    # this should exit
    with pytest.raises(ValueError):
        get_fh("does_not_exist.txt", "rrr")
