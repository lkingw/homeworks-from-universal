#!/usr/bin/env python3
# intersection.py
"""
This program finds all gene symbols that appear both in the
chr21_genes.txt file and in the HUGO_genes.txt file, and then print out
the number of unique genes and intersection
"""

import argparse
from assignment4 import my_io


def main():
    """Business Logic"""
    args = get_cli_args()
    infile1 = args.infile1
    infile2 = args.infile2
    fh_in = my_io.get_fh(infile1, "r")
    fh_in2 = my_io.get_fh(infile2, "r")
    fh_out = my_io.get_fh("OUTPUT/intersection_output.txt", "w")
    gene_list1, gene_list2 = find_gene_lists(fh_in, fh_in2)
    unique_list1, unique_list2 = find_unique_gene(gene_list1, gene_list2)
    common_list = find_intersection(unique_list1, unique_list2, fh_out)
    print_result(infile1, infile2, unique_list1, unique_list2, common_list)


def find_gene_lists(fh_in, fh_in2):
    """
    get two gene lists from two txt files
    """
    gene_list1 = []
    gene_list2 = []
    lines1 = fh_in.readlines()[1:]
    lines2 = fh_in2.readlines()[1:]
    for line in lines1:
        gene1 = line.replace("\n", "").split("\t")[0]
        gene_list1.append(gene1)
    for line in lines2:
        gene2 = line.replace("\n", "").split("\t")[0]
        gene_list2.append(gene2)
    return gene_list1, gene_list2


def find_unique_gene(gene_list1, gene_list2):
    """
    Find their unique gene lists from the original lists
    """
    unique_list1 = list(set(gene_list1))
    unique_list2 = list(set(gene_list2))
    return unique_list1, unique_list2


def find_intersection(unique_list1, unique_list2, fh_out):
    """
    Find the intersection between two unique lists and sort it
    """
    intersection = set(unique_list1).intersection(set(unique_list2))
    common_list = sorted(list(intersection))
    for item in common_list:
        fh_out.write("%s\n" % item)
    return common_list


def print_result(infile1, infile2, unique_list1, unique_list2, common_list):
    """
    Print the result of the number of unique genes and their intersection
    """
    print(f"\nNumber of unique gene names in {infile1}: {len(unique_list1)}")
    print(f"Number of unique gene names in {infile2}: {len(unique_list2)}")
    print(f"Number of common gene symbols found: {len(common_list)}")
    print(f"Output stored in OUTPUT/intersection_output.txt")


def get_cli_args():
    """
    Just get the command line options using argparse
    @return: Instance of argparse arguments
    """
    parser = argparse.ArgumentParser(description='Provide two gene list (ignore header line), \
find intersection')
    parser.add_argument('-i1', '--infile1', dest='infile1',
                        type=str, help='Gene list 1 to open',
                        required=False, default='chr21_genes.txt')
    parser.add_argument('-i2', '--infile2', dest='infile2',
                        type=str, help='Gene list 2 to open',
                        required=False, default='HUGO_genes.txt')

    return parser.parse_args()


if __name__ == '__main__':
    main()
