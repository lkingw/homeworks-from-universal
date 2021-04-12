#!/usr/bin/python3

"""
Test suite for config.py
"""
from assignment5 import config

# pylint: disable=C0116
# pylint: disable=C0103


def test_get_host_keyword():
    """
    does host keyword convert correctly
    """
    assert config.get_host_keyword()['cow'] == "Bos_taurus"
    assert config.get_host_keyword()['human'] == "Homo_sapiens"
    assert config.get_host_keyword()['sheep'] == "Ovis_aries"


def test_get_unigene_directory():
    """
    does the data directory is correct
    """
    assert config.get_unigene_directory() == "/data/PROGRAMMING/assignment5"


def test_get_unigene_extension():
    """
    does the file extension is correct
    """
    assert config.get_unigene_extension() == "unigene"


def test_error_messages_print():
    """
    test whether the two error print functions are work well
    """
    assert config.get_error_string_4_not_found_gene_for_host('Cow', 'API5') is None
    assert config.get_error_string_4_not_found_host() is None
