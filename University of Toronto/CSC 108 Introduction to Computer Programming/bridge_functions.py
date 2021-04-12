"""CSC108H1S: Functions for Assignment 2 - Bridges.

Instructions (READ THIS FIRST!)
===============================

Make sure that the file a2_checker.py, and the directory pyta, are in the same
directory as this file.

The data used for this assignment is a subset of the data found in:
https://www.ontario.ca/data/bridge-conditions

Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students
taking the CSC108 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Tom Fairgrieve, Amanjit Kainth, Kaveh Mahdaviani,
Sadia Sharmin, and Joseph Jay Williams
"""
from typing import List

import csv
import math

################################################################################
# Begin constants
################################################################################
COLUMN_ID = 0
COLUMN_NAME = 1
COLUMN_HIGHWAY = 2
COLUMN_LAT = 3
COLUMN_LON = 4
COLUMN_YEAR_BUILT = 5
COLUMN_LAST_MAJOR_REHAB = 6
COLUMN_LAST_MINOR_REHAB = 7
COLUMN_NUM_SPANS = 8
COLUMN_SPAN_DETAILS = 9
COLUMN_DECK_LENGTH = 10
COLUMN_LAST_INSPECTED = 11
COLUMN_BCI = 12

INDEX_BCI_YEARS = 0
INDEX_BCI_SCORES = 1
MISSING_BCI = -1.0

EARTH_RADIUS = 6371


################################################################################
# Sample data for docstring examples
################################################################################
def create_example_bridge_1() -> list:
    """Return a bridge in our list-format to use for doctest examples.

    This bridge is the same as the bridge from row 3 of the dataset.
    """

    return [
        1, 'Highway 24 Underpass at Highway 403',
        '403', 43.167233, -80.275567, '1965', '2014', '2009', 4,
        [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
        [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
          '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
         [MISSING_BCI, 72.3, MISSING_BCI, 69.5, MISSING_BCI, 70.0, MISSING_BCI,
          70.3, MISSING_BCI, 70.5, MISSING_BCI, 70.7, 72.9, MISSING_BCI]]
    ]


def create_example_bridge_2() -> list:
    """Return a bridge in our list-format to use for doctest examples.

    This bridge is the same as the bridge from row 4 of the dataset.
    """

    return [
        2, 'WEST STREET UNDERPASS',
        '403', 43.164531, -80.251582, '1963', '2014', '2007', 4,
        [12.2, 18.0, 18.0, 12.2], 61.0, '04/13/2012',
        [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
          '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
         [MISSING_BCI, 71.5, MISSING_BCI, 68.1, MISSING_BCI, 69.0, MISSING_BCI,
          69.4, MISSING_BCI, 69.4, MISSING_BCI, 70.3, 73.3, MISSING_BCI]]
    ]


def create_example_bridge_3() -> list:
    """Return a bridge in our list-format to use for doctest examples.

    This bridge is the same as the bridge from row 33 of the dataset.
    """

    return [
        3, 'STOKES RIVER BRIDGE', '6',
        45.036739, -81.33579, '1958', '2013', '', 1,
        [16.0], 18.4, '08/28/2013',
        [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
          '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
         [85.1, MISSING_BCI, 67.8, MISSING_BCI, 67.4, MISSING_BCI, 69.2,
          70.0, 70.5, MISSING_BCI, 75.1, MISSING_BCI, 90.1, MISSING_BCI]]
    ]


def create_example_bridges() -> List[list]:
    """Return a list containing three unique example bridges.

    The bridges contained in the list are from row 3, 4, and 33 of the dataset
    (in that order).
    """
    return [
        create_example_bridge_1(),
        create_example_bridge_2(),
        create_example_bridge_3()
    ]


################################################################################
# Helper function
################################################################################
def calculate_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by
    (lat1, lon1) and (lat2, lon2), rounded to the nearest meter.

    >>> calculate_distance(43.659777, -79.397383, 43.657129, -79.399439)
    0.338
    >>> calculate_distance(43.42, -79.24, 53.32, -113.30)
    2713.226
    """

    # This function uses the haversine function to find the
    # distance between two locations. You do NOT need to understand why it
    # works. You will just need to call on the function and work with what it
    # returns.
    # Based on code at goo.gl/JrPG4j

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1),
                              math.radians(lon2), math.radians(lat2))

    # haversine formula t
    lon_diff = lon2 - lon1
    lat_diff = lat2 - lat1
    a = (math.sin(lat_diff / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return round(c * EARTH_RADIUS, 3)


################################################################################
# Part 1 - Querying the data
################################################################################
def find_bridge_by_id(bridges: List[list], bridge_id: int) -> list:
    """Return the data for the bridge with id bridge_id from bridges.

    If there is no bridge with the given id in bridges, then return an empty
    list.

    >>> example_bridges = create_example_bridges()
    >>> find_bridge_by_id(example_bridges, 4)
    []
    >>> find_bridge_by_id(example_bridges, 2) == create_example_bridge_2()
    True
    """
    ret = []
    for bridge in bridges:
        if bridge[COLUMN_ID] == bridge_id:
            ret = bridge
            break

    return ret


def find_bridges_in_radius(bridges: List[list], lat: float, lon: float,
                           radius: int, exclusions: List[int]) -> List[int]:
    """Return the IDs of the bridges that are within radius kilometres from
    location (lat, lon). Include bridge IDs that are exactly radius kilometres
    away. The bridge IDs in exclusions are not included in the result.

    Preconditions:
        - (lat, lon) is a valid location on Earth
        - radius > 0

    >>> example_bridges = create_example_bridges()
    >>> find_bridges_in_radius(example_bridges, 43.10, -80.15, 50, [])
    [1, 2]
    >>> find_bridges_in_radius(example_bridges, 43.10, -80.15, 50, [1, 2])
    []
    """

    ret = []
    for bridge in bridges:
        bridge_lat = bridge[COLUMN_LAT]
        bridge_lon = bridge[COLUMN_LON]
        _dis = calculate_distance(bridge_lat, bridge_lon, lat, lon)
        if _dis <= radius:
            if bridge[COLUMN_ID] not in exclusions:
                ret.append(bridge[COLUMN_ID])
        
    return ret


def get_bridge_condition(bridges: List[list], bridge_id: int) -> float:
    """Return the most recent BCI score of the bridge in bridges with id
    bridge_id.

    The most recent BCI score is the BCI score given to the bridge in the
    highest (i.e., most recent) year. If there is no score for every year,
    return MISSING_BCI.

    >>> example_bridges = create_example_bridges()
    >>> get_bridge_condition(example_bridges, 1)
    72.3
    """
    rct_bci_val = MISSING_BCI
    for bridge in bridges:
        if bridge[COLUMN_ID] == bridge_id:
            bct_mat = bridge[COLUMN_BCI]
            bci_val = bct_mat[1]
            for _val in bci_val:
                if _val is not MISSING_BCI:
                    rct_bci_val = _val
                    break

    return rct_bci_val


def calculate_average_condition(bridge: list, start: int, stop: int) -> float:
    """Return the average BCI score of bridge between the year start (inclusive)
    and stop (exclusive).

    Scores with the value MISSING_BCI are invalid and should not be included in
    the average. If there are no valid scores between start and stop, return
    0.0.

    Preconditions:
        - start > 0
        - start <= stop

    >>> bridge_1 = create_example_bridge_1()
    >>> calculate_average_condition(bridge_1, 2005, 2013)
    70.525
    >>> calculate_average_condition(bridge_1, 2013, 2021)
    0.0
    """

    _counter = 0
    tol_bci_val = 0
    bci_mat = bridge[COLUMN_BCI]
    bci_yrs = bci_mat[INDEX_BCI_YEARS]
    bci_val = bci_mat[INDEX_BCI_SCORES]

    for i in range(len(bci_yrs)):
        _yr = int(bci_yrs[i])
        if start <= _yr < stop:
            _val = bci_val[i]
            if _val is not MISSING_BCI:
                _counter += 1
                tol_bci_val += _val

    if _counter > 0:
        return tol_bci_val / _counter
    else: return 0.0


################################################################################
# Part 2 - Mutating the data
################################################################################
def inspect_bridge(bridges: List[list], bridge_id: int, date: str,
                   bci: float) -> None:
    """Update the bridge in bridges with id bridge_id so that it is last
    inspected at the new date date and its most recent BCI score is bci in the
    year given by date.

    Precondition:
        - bridges contains a bridge with id bridge_id
        - date is in the format 'MM/DD/YYYY'
        - 0.0 <= bci <= 100.0

    >>> my_bridge = create_example_bridge_1()
    >>> inspect_bridge([my_bridge], 1, '02/14/2021', 71.9)
    >>> my_bridge[COLUMN_LAST_INSPECTED]
    '02/14/2021'
    >>> my_bridge[COLUMN_BCI][INDEX_BCI_YEARS][0]
    '2021'
    >>> my_bridge[COLUMN_BCI][INDEX_BCI_SCORES][0]
    71.9
    """

    for bridge in bridges:
        if bridge[COLUMN_ID] == bridge_id:
           bridge[COLUMN_LAST_INSPECTED] = date
           if date != '':
               _year = date.split('/')[2]
               if len(bridge[COLUMN_BCI][INDEX_BCI_YEARS]) < 1 \
                    or bridge[COLUMN_BCI][INDEX_BCI_YEARS][0] != _year:
                   bridge[COLUMN_BCI][INDEX_BCI_YEARS][:0] = [_year] 
                   bridge[COLUMN_BCI][INDEX_BCI_SCORES][:0] = [bci]
               else:
                   bridge[COLUMN_BCI][INDEX_BCI_SCORES][0] = bci


def rehabilitate_bridge(bridges: List[list], bridge_ids: List[int],
                        new_year: str, is_major: bool) -> None:
    """Update the bridges with ids from bridge_ids in bridges to have their
    last rehab set to new_year. If is_major is True, update the major rehab
    date. Otherwise, update the minor rehab date.

    Precondition:
        - bridges contains the bridges with the ids in bridge_ids

    >>> my_bridge = create_example_bridge_1()
    >>> rehabilitate_bridge([my_bridge], [1], '2021', False)
    >>> my_bridge[COLUMN_LAST_MINOR_REHAB]
    '2021'
    """

    for bridge in bridges:
        for bridge_id in bridge_ids:
            if bridge[COLUMN_ID] == bridge_id:
                if is_major is True:
                    bridge[COLUMN_LAST_MAJOR_REHAB] = new_year
                else:
                    bridge[COLUMN_LAST_MINOR_REHAB] = new_year


################################################################################
# Part 3 - Implementing useful algorithms
################################################################################
def find_worst_bci(bridges: List[list], bridge_ids: List[int]) -> int:
    """Return the bridge ID from bridge_ids of the bridge from bridges who
    has the lowest most recent BCI score.

    If there is a tie, return the bridge with the smaller bridge ID in bridges.

    Precondition:
        - bridges contains the bridges with the ids in bridge_ids
        - every bridge in bridges has at least one BCI score
        - the IDs in bridge_ids appear in increasing order

    >>> example_bridges = create_example_bridges()
    >>> find_worst_bci(example_bridges, [1, 2])
    2
    >>> find_worst_bci(example_bridges, [1, 3])
    1
    """
    worst_bci = 100
    worst_brd_id = bridge_ids[0]
    for bridge in bridges:
        for bridge_id in bridge_ids:
            if bridge[COLUMN_ID] == bridge_id:
                bct_val = bridge[COLUMN_BCI][INDEX_BCI_SCORES]
                rst_bci = next((el for el in bct_val if el is not MISSING_BCI) \
                    , MISSING_BCI)
                if rst_bci < worst_bci:
                    worst_brd_id = bridge_id
                    worst_bci = rst_bci
    
    return worst_brd_id


def map_route(bridges: List[list], lat: float, lon: float,
              max_bridges: int, radius: int) -> List[int]:
    """Return the sequence of bridge IDs from bridges that must be visited
    by an inspector who initially starts at location (lat, lon). The sequence
    must contain at most max_bridges IDs. Every ID in the sequence must be
    unique; an inspector cannot inspect the same bridge twice.

    The inspector visits the bridge within radius of their location that has
    the lowest most recent BCI score. The next bridge inspected is the bridge
    with the lowest most recent BCI score within radius radius of the last
    bridge's location. This step repeats until max_bridges bridges have been
    inspected, or there are no bridges to inspect within radius.

    >>> example_bridges = create_example_bridges()
    >>> map_route(example_bridges, 43.10, -80.15, 3, 50)
    [2, 1]
    >>> map_route(example_bridges, 43.1, -80.5, 30, 10)
    []
    """
    _label = True
    pos = [lat, lon] 
    _route = []
    next_bridge = ''
    while _label is True and len(_route) < max_bridges:
        low_rst_bci = 100
        low_bci_id = ''
        _label = False
        for bridge in bridges:
            _dis = calculate_distance(pos[0], pos[1], \
                 bridge[COLUMN_LAT], bridge[COLUMN_LON])
            if _dis <= radius and bridge[COLUMN_ID] is not next_bridge:
                _label = True
                bct_val = bridge[COLUMN_BCI][INDEX_BCI_SCORES]
                rst_bci = next((el for el in bct_val if el is not MISSING_BCI) \
                    , MISSING_BCI)
                if rst_bci is not MISSING_BCI and rst_bci < low_rst_bci \
                    and bridge[COLUMN_ID] not in _route:
                    pos[0] = bridge[COLUMN_LAT]
                    pos[1] = bridge[COLUMN_LON]
                    next_bridge = bridge[COLUMN_ID]
                    low_bci_id = bridge[COLUMN_ID]
                    low_rst_bci = rst_bci

        if low_bci_id != '':
            _route.append(low_bci_id)

    return _route

################################################################################
# Part 4 - Reading and cleaning raw data
################################################################################
def clean_length_data(raw_length: str) -> float:
    """Return the length of the bridge based on the value in raw_length.

    If raw_length is an empty string, return 0.0.

    Precondition:
        - if raw_length is not the empty string, it can be converted to a float

    >>> clean_length_data('12')
    12.0
    """

    if raw_length == '':
        return 0.0
    else:
        return float(raw_length)


def trim_from_end(raw_data: list, count: int) -> None:
    """Update raw_data so that count elements have been removed from the end.

    Preconditions:
        - count >= 0
        - len(raw_data) >= count

    >>> my_lst = [[72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9], '', '72.3', '', \
    '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9', '']
    >>> trim_from_end(my_lst, 14)
    >>> my_lst
    [[72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    """
    while(count):
        count -= 1
        raw_data.pop()


def clean_span_data(raw_spans: str) -> List[float]:
    """Return a list of span lengths from raw_spans, in the same order that
    they appear in raw_spans.

    Precondition:
        - raw_spans is in the appropriate format (see handout for details)

    >>> clean_span_data('Total=64  (1)=12;(2)=19;(3)=21;(4)=12;')
    [12.0, 19.0, 21.0, 12.0]
    """

    data_list = []
    raw_spans = raw_spans.split('  ')[1]
    spans = raw_spans.split(';')
    for span in spans:
        if len(span.split('=')) > 1:
            data = span.split('=')[1]
            data_list.append(float(data))

    return data_list

def clean_bci_data(bci_years: List[str], start_year: int, bci_scores: list) -> \
        None:
    """Update bci_years so that each element contains the year as a string,
    starting from start_year and decreasing by one for each subsequent element,
    until bci_years has the same length as bci_scores. Also update bci_scores
    so that all non-empty string values are float values, and all empty string
    values are MISSING_BCI.

    Preconditions:
        - len(bci_years) == 0
        - len(bci_scores) > 0
        - start_year - len(bci_scores) >= 0
        - every value in bci_scores is either an empty string or can be
        converted to a float

    >>> years = []
    >>> scores = ['', '72.3', '', '69.5', '', '70.0', '', '70.3', '']
    >>> clean_bci_data(years, 2013, scores)
    >>> years
    ['2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005']
    >>> scores
    [-1.0, 72.3, -1.0, 69.5, -1.0, 70.0, -1.0, 70.3, -1.0]
    """
    
    for i in range(len(bci_scores)):
        if bci_scores[i] == '':
            bci_scores[i] = -1.0
            bci_years.append(str(start_year - i))
        else:
            bci_scores[i] = float(bci_scores[i])
            bci_years.append(str(start_year - i))


def clean_data(data: List[list], start_year: int) -> None:
    """Update data so that the applicable string values are converted to their
    appropriate type. In addition, update COLUMN_ID for each inner list so that
    the first inner list has an ID of 1 and each subsequent inner list has an
    ID of 1 more than the last inner list.

    The indexes of the string values that are converted, and their
    corresponding type, are:
        - COLUMN_LAT is a float
        - COLUMN_LON is a float
        - COLUMN_LENGTH is a float
        - COLUMN_NUM_SPANS is an int
        - COLUMN_SPAN_LENGTH is a list of floats
        - COLUMN_BCIS is a list of floats

    >>> raw_bridge_1 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', \
    '403', '43.167233', '-80.275567', '1965', '2014', '2009', '4', \
    'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', \
    '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', \
    '70.7', '72.9', '']
    >>> clean_data([raw_bridge_1], 2013)
    >>> raw_bridge_1 == create_example_bridge_1()
    True
    """

    next_id = 1

    for row in data:
        row[COLUMN_ID] = next_id
        next_id = next_id + 1

        row[COLUMN_LAT] = float(row[COLUMN_LAT])
        row[COLUMN_LON] = float(row[COLUMN_LON])
        row[COLUMN_NUM_SPANS] = int(row[COLUMN_NUM_SPANS])
        row[COLUMN_DECK_LENGTH] = clean_length_data(row[COLUMN_DECK_LENGTH])
        row[COLUMN_SPAN_DETAILS] = clean_span_data(row[COLUMN_SPAN_DETAILS])

        bci_years = []
        bci_scores = row[COLUMN_BCI + 1:]
        clean_bci_data(bci_years, start_year, bci_scores)
        row[COLUMN_BCI] = [bci_years, bci_scores]

        trim_from_end(row, len(row) - COLUMN_BCI - 1)


def read_data(filename: str) -> List[list]:
    """Return the data found in the file filename as a list of lists.

    Each inner list corresponds to a row in the file that has been cleaned with
    clean_data.

    Docstring examples not given since the results depend on filename.

    Preconditions:
        - The data in filename is in a valid format
    """
    with open(filename) as csv_file:
        lines = list(csv.reader(csv_file))

        start_year = int(lines[1][COLUMN_BCI + 1])

        data = lines[2:]
        clean_data(data, start_year)

    return data


if __name__ == '__main__':
    # Automatically run all doctest examples to see if any fail
    import doctest
    #doctest.testmod()

    my_bridge = create_example_bridge_1()
    inspect_bridge([my_bridge], 1, '02/14/2021', 71.9)
    print(my_bridge[COLUMN_LAST_INSPECTED])
    #'02/14/2021'
    print(my_bridge[COLUMN_BCI][INDEX_BCI_YEARS][0])
    #'2021'
    print(my_bridge[COLUMN_BCI][INDEX_BCI_SCORES][0])
    #71.9
    print(my_bridge)
    # To test your code with the actual dataset, uncomment the code below
    # bridges_small = read_data('bridge_data_small.csv')

    # To test your code with the whole actual dataset, uncomment the code below
    # bridges_large = read_data('bridge_data_large.csv')
