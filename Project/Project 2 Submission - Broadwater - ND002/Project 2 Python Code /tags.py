#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid
keys in MongoDB,as well as see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters. Please complete the function 'key_type'.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, tags, keys, others, problems):
    if element.tag == "tag":
        # YOUR CODE HERE

        # Iterate through each tag in the current "tag" element, test if
        # the "k" value matches any of our regular expressions, and count
        # how many matches we find for each.
        for tag in element.iter():
            tags.add(tag.attrib['k'])
            if lower.search(tag.attrib['k']) is not None:
                keys.update([("lower", (keys["lower"] + 1))])
            elif lower_colon.search(tag.attrib['k']) is not None:
                keys.update([("lower_colon", (keys["lower_colon"] + 1))])
            elif problemchars.search(tag.attrib['k']) is not None:
                keys.update([("problemchars", (keys["problemchars"] + 1))])
                problems.add(tag.attrib['k'])
            else:
                keys.update([("other", (keys["other"] + 1))])
                others.add(tag.attrib['k'])
    return tags, keys, others, problems


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    others = set()
    problems = set()
    tags = set()
    for _, element in ET.iterparse(filename):
        tags, keys, others, problems = key_type(
            element, tags, keys, others, problems)

    return tags, keys, others, problems


def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    tags, keys, others, problems = process_map('san_diego.osm.xml')
    pprint.pprint(tags)
    pprint.pprint(keys)
    pprint.pprint(others)
    pprint.pprint(problems)


if __name__ == "__main__":
    test()
