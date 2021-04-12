#!/usr/bin/env python3
# descriptive_statistics.py
"""In this program, we opened three files and calculated required statistics on
the column specified by the command line"""

import sys
from math import isnan

#Define functions to calculate statistics that are required in this program
def cal_ave(numbers):
    """Calculate the average of the numbers"""
    return sum(numbers) / len(numbers)


def cal_vari(numbers, average):
    """Calculate the variance of the numbers"""
    if len(numbers) == 1:
        return 0
    return sum((i-float(average)) ** 2 for i in numbers) / (len(numbers)-1)


def cal_sd(numbers, average):
    """Calculate the standard deviation of the numbers"""
    if len(numbers) == 1:
        return 0
    return cal_vari(numbers, average) ** 0.5


def cal_median(numbers):
    """Calculate the median of the numbers"""
    numbers_sorted = sorted(numbers)
    validnum = len(numbers)
    if validnum % 2 == 0:
        medium1 = numbers_sorted[validnum // 2]
        medium2 = numbers_sorted[(validnum // 2)-1]
        medium = (medium1 + medium2) / 2
    else:
        medium = numbers_sorted[validnum // 2]
    return medium


def cal_minmax(numbers):
    """Find the minimum and maximum of the numbers"""
    return min(numbers), max(numbers)


def main():
    """Business logic"""
    #Input file
    file = sys.argv[1]
    #The column to parse
    column_to_parse = int(sys.argv[2])
    #Build an empty list to store the data
    numbers = []
    count = 0
    #loop over a file and store the data from a column in the list
    #Leave an error message if arguments cannot pass into the programmer
    with open(file, 'r') as infile:
        for line in infile:
            count += 1
            try:
                #Split the line that we are looping into
                num = float(line.split("\t")[column_to_parse])
                if not isnan(num):
                    numbers.append(num)
            #Print out error messages if errors happen
            except ValueError:
                print("\n Skipping line number {} : could not convert string to \
float: '{}' \n".format(count, line.split("\t")[column_to_parse]))
                continue
            except IndexError:
                print("\n Exiting: There is no valid 'list index' in column {} in line {} in \
file: {}".format(column_to_parse, count, file))
                sys.exit()

    if len(numbers) < 1:
        print("\n Error: There were no valid number(s) in column {} in \
file: {}".format(column_to_parse, file))
        sys.exit()

    results = dict()
    results['Count'] = count
    results['ValidNum'] = len(numbers)
    results['Average'] = cal_ave(numbers)
    results['Variance'] = cal_vari(numbers, results['Average'])
    results['Minimum'], results['Maximum'] = cal_minmax(numbers)
    results['Median'] = cal_median(numbers)
    results['Std Dev'] = cal_sd(numbers, results['Average'])

    print('    Column: {} \n \n'.format(column_to_parse))
    for k in ['Count', 'ValidNum', 'Average', 'Maximum', 'Minimum',
              'Variance', 'Std Dev', 'Median']:
        print(' ' * 8, end='')
        print('{:10}={:10.3f}'.format(k, results[k]))


main()
