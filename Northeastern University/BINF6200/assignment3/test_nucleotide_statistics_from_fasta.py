#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Test suit for nucleotide_statistics_from_fasta.py"""
import os
import pytest
from nucleotide_statistics_from_fasta import get_fh, \
    get_header_and_sequence_lists, _check_size_of_lists, \
    print_sequence_stats, _get_nt_occurrence, _get_accession

# pylint: disable=C0116
# pylint: disable=C0103

FILE_2_TEST = 'ss.txt'
FASTA_STRING = \
    """
>EU521893 A/Arequipa/FLU3833/2006 2006// 4 (HA)
AACAGCACGGCAACGCTGTGCCTTGGGCACCATGCAGTACCAAACGGAACGATAGTGAAAACAATCACGA
ATGACCAAATTGAAGTTACTAATGCTACTGAGCTGGTTCAGAGTTCCTCAACAGGTGAAATATGCGACAG
TCCTCATCAGATCCTTGATGGAGAAAACTGCACACTAATAGATGCTCTATTGGGAGACCCTCAGTGTGAT
>EU521806 A/Arequipa/FLU3836/2006 2006// 4 (HA)
ATAAAAGCAACCAAAATGAAAGTAAAACTACTGGTTCTGTTATGTACATTTACAGCTACATATGCAGACA
CAATATGTATAGGCTACCATGCCAACAATTCAACCGACACTGTTGACACAGTACTTGAGAAGAATGTGAC
AGTGACACACTCTGTCAACCTACTTGAGGACAGTCACAATGGAAAACTATGTCTACTAAAAGGAATAGCC
>EU521894 A/Arequipa/FLU3845/2006 2006// 4 (HA)
ACGGCAACGCTGTGCCTTGGGCACCATGCAGTACCAAACGGAACGATAGTGAAAACAATCACGAATGACC
AAATTGAAGTTACTAATGCTACTGAGCTGGTTCAGAGTTCCTCAACAGGTGAAATATGCGACAGTCCTCA
TCAGATCCTTGATGGAGAAAACTGCACACTAATAGATGCTCTATTGGGAGACCCTCAGTGTGATGGCTTC
"""


def test_existing_get_fh_4_reading():

    # does it open a file for reading

    test = get_fh(FILE_2_TEST, 'r')
    assert hasattr(test, 'readline') is True, \
        'Not able to open for reading'


def test_existing_get_fh_4_wrting():

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

    expected_header = '>EU521893 A/Arequipa/FLU3833/2006 2006// 4 (HA)'
    expected_sequence = \
        """
    AACAGCACGGCAACGCTGTGCCTTGGGCACCATGCAGTACCAAACGGAACGATAGTGAAAACAATCACGA
    ATGACCAAATTGAAGTTACTAATGCTACTGAGCTGGTTCAGAGTTCCTCAACAGGTGAAATATGCGACAG
    TCCTCATCAGATCCTTGATGGAGAAAACTGCACACTAATAGATGCTCTATTGGGAGACCCTCAGTGTGAT
    """
    expected_sequence = expected_sequence.replace(' ', '').replace('\n', '')
    test = open('test2.txt', 'w')
    test.write(FASTA_STRING)
    test.close()
    data = get_fh('test2.txt', 'r')
    (headers, seqs) = get_header_and_sequence_lists(data)
    data.close()
    os.remove('test2.txt')
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
        assert e.type == SystemExit, 'Not exit'
        assert e.value.code == 1, 'Not correctly exit'


def test_print_sequence_stats():

    # does it print correctly header and stats data to file

    expected_header = \
        "Number\tAccession\tA's\tG's\tC's\tT's\tN's\tLength\tGC%\n"
    expected_stats = '1\tEU521893\t68\t48\t48\t46\t0\t210\t45.7\n'
    test = open('test2.txt', 'w')
    test.write(FASTA_STRING)
    test.close()
    data = get_fh('test2.txt', 'r')
    (headers, seqs) = get_header_and_sequence_lists(data)
    data.close()
    os.remove('test2.txt')

    out = get_fh('out.txt', 'w')
    print_sequence_stats(headers, seqs, out)
    out.close()

    testOut = get_fh('out.txt', 'r')
    assert hasattr(testOut, 'readline') is True, \
        'No output file generated'

    assert testOut.readline() == expected_header, 'Written header error'
    assert testOut.readline() == expected_stats, 'Written stats error'
    testOut.close()


def test_get_nt_occurrence_for_count():

    # does it count nt corretly

    sequence = 'AACAGCACGGCAACGCTG122!vvvvvNNN'
    numA = _get_nt_occurrence('A', sequence)
    numT = _get_nt_occurrence('T', sequence)
    numC = _get_nt_occurrence('C', sequence)
    numG = _get_nt_occurrence('G', sequence)
    numN = _get_nt_occurrence('N', sequence)
    assert numA == 6, 'Wrong number for A'
    assert numT == 1, 'Wrong number for T'
    assert numC == 6, 'Wrong number for C'
    assert numG == 5, 'Wrong number for G'
    assert numN == 3, 'Wrong number for N'


def test_get_nt_occurrence_for_exit():

    # does it exit when encounter an unexpected nt type

    sequence = 'AACAGCACGGCAACGCTG122!vvvvvNNN'
    with pytest.raises(SystemExit) as e:
        _get_nt_occurrence('0', sequence)
        assert e.type == SystemExit, 'Not correctly exit'
        assert e.value.code == 1, 'Not correctly exit'


def test_get_accession():

    # does it get right accession info in a header

    header = '>EU521893 A/Arequipa/FLU3833/2006 2006// 4 (HA)'
    acc = _get_accession(header)
    assert acc == 'EU521893', 'Wrong accession obtained'
