#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""


def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        # Iterate through each event and element and count
        # the number of times each user appears in the "uid" tag.
        for tag in element.iter():
            if "uid" in tag.attrib:
                users.add(tag.attrib['uid'])
    return users


def test():

    users = process_map('san_diego.osm.xml')
    pprint.pprint(users)
    print len(users)


if __name__ == "__main__":
    test()
