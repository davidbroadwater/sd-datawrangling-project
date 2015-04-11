#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
        # YOUR CODE HERE

        tags = {}
        # Iterate through each event and element and count 
        # the number of times each tag appears.
        for event, elem in ET.iterparse(filename):
            if elem.tag in tags:
                tags.update([(elem.tag, (tags[elem.tag] + 1))])
            else:
                tags.update([(elem.tag, 1)])
        return tags 

def map_parser():

    tags = count_tags('san_diego.osm.xml')
    pprint.pprint(tags)

    

if __name__ == "__main__":
    map_parser()