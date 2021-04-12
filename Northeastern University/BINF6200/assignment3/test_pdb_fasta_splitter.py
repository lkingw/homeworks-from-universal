#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Test suit for pdb_fasta_splitter.py"""
import os
import pytest
from pdb_fasta_splitter import get_fh, get_header_and_sequence_lists, \
    _check_size_of_lists

# pylint: disable=C0116
# pylint: disable=C0103

FILE_2_TEST = 'ss.txt'
FASTA_STRING = \
    """
>101M:A:sequence
MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGA
ILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKEL
GYQG
>101M:A:secstr
    HHHHHHHHHHHHHHGGGHHHHHHHHHHHHHHH GGGGGG TTTTT  SHHHHHH HHHHHHHHHHHHHHHH
HHTTTT  HHHHHHHHHHHHHTS   HHHHHHHHHHHHHHHHHH GGG SHHHHHHHHHHHHHHHHHHHHHHHHT
T   
>102L:A:sequence
MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAA
VRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRV
ITTFRTGTWDAYKNL
"""


def test_existing_get_fh_4_reading():

    # does it open a file for reading

    test = get_fh(FILE_2_TEST, 'r')
    assert hasattr(test, 'readline') is True, \
        'Not able to open for reading'


def test_existing_get_fh_4_wring():

    # does it open a file for wrting

    test = get_fh('test.txt', 'w')
    assert hasattr(test, 'write') is True, \
        'Not able to open for writing'
    test.close()
    os.remove('test.txt')


def test_get_fh_4_IOError():

    # does it raise IOError

    with pytest.raises(IOError):
        get_fh('does_not_exist.txt', 'r')


def test_get_fh4_ValueError():

    # does it raise ValueError

    with pytest.raises(ValueError):
        get_fh('wrong_open_mode.txt', 'rrr')


def test_get_header_and_sequence():

    # does it correctly recognize header and sequence from a string

    expected_header = '>101M:A:sequence'
    expected_sequence = \
        """
    MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGA
    ILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKEL
    GYQG
    """
    expected_sequence = expected_sequence.replace(' ', '').replace('\n', '')
    test = open('test.txt', 'w')
    test.write(FASTA_STRING)
    test.close()
    data = get_fh('test.txt', 'r')
    (headers, seqs) = get_header_and_sequence_lists(data)
    data.close()
    os.remove('test.txt')
    assert headers[0] == expected_header, 'Wrong header obtained'
    assert seqs[0] == expected_sequence, 'Wrong sequence obtained'


def test_check_size_of_lists_for_comparison():

    # does it correctly compare lengths of two lists

    test = open('test2.txt', 'w')
    test.write(FASTA_STRING)
    test.close()
    data = get_fh('test2.txt', 'r')
    (headers, seqs) = get_header_and_sequence_lists(data)
    data.close()
    os.remove('test2.txt')
    assert _check_size_of_lists(headers, seqs) is True, \
        'List size check error'


def test_check_size_of_lists_for_exit():

    # does it exit when lengths of two input lists are not equal

    test = open('test2.txt', 'w')
    test.write(FASTA_STRING)
    test.close()
    data = get_fh('test2.txt', 'r')
    (headers, seqs) = get_header_and_sequence_lists(data)
    data.close()
    os.remove('test2.txt')
    with pytest.raises(SystemExit) as e:
        _check_size_of_lists(headers, seqs.pop())
        assert e.type == SystemExit, 'Not correctly exit'
        assert e.value.code == 1, 'Not correctly exit'
