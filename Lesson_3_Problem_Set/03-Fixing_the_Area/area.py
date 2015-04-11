#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def most_significant_number(num_string):

    reader = csv.reader([num_string], delimiter='|')
    values = []
    sig_figs = []
    for item in reader:
        for s in item:
            values.append(s.strip('{}'))

    for num_string in values:
        if '.' in num_string:
            # Has decimal point. Include in sig fig calculations
            sig_figs.append(len(num_string.partition('e')[0]))
        else:
            # No decimal point. Count trailing zeros.
            sig_figs.append(len(num_string.partition('e')[0].rstrip('0')))

    max_sig_figs = max(sig_figs)
    i = sig_figs.index(max_sig_figs)
    return float(values[i])


def fix_area(area):

    # YOUR CODE HERE
    if (area == "NULL") or (area == ""):
        area = None
    elif area.startswith("{"):
        area = most_significant_number(area)
    elif is_float(area):
        area = float(area)
    else:
        area = None
    return area



def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra matadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[8]["areaLand"] == 55166700.0
    assert data[3]["areaLand"] == None


if __name__ == "__main__":
    test()