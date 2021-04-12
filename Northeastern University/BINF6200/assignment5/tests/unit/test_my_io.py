#!/usr/bin/python3

"""
Test suite for my_io.py
"""
import pytest
from assignment5 import my_io

# pylint: disable=C0116
# pylint: disable=C0103

FILE_2_TEST = '/data/PROGRAMMING/assignment5/Homo_sapiens/TIMM9.unigene'


def test_existing_get_fh_4_reading():
    """
    does it open a file for reading
    """
    test = my_io.get_fh(FILE_2_TEST, "r")
    assert hasattr(test, "readline") is True, "Not able to open for reading"


def test_get_fh_4_IOError():
    """
    does it raise IOError
    this should exit
    """
    with pytest.raises(IOError):
        my_io.get_fh("does_not_exist.txt", "r")


def test_get_fh_4_ValueError():
    """
    does it raise ValueError
    this should exit
    """
    with pytest.raises(ValueError):
        my_io.get_fh("does_not_exist.txt", "rrr")


def test_get_fh_4_TypeError():
    """
    does it raise on TypeError
    this should exit
    """
    with pytest.raises(TypeError):
        my_io.get_fh([], "r")


def test_is_valid_gene_file_name():
    """
    does the function can identify a path is valid correctly
    """
    assert my_io.is_valid_gene_file_name(FILE_2_TEST) is True
    assert my_io.is_valid_gene_file_name('') is False
