#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
[x] you should process only 2 types of top level tags: "node" and "way"
[x] all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    [x] attributes in the CREATED array should be added under a key "created"
    [x] attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
[x] if second level tag "k" value contains problematic characters, it should be ignored
[x] if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
[] if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
[x] if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

[x] for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE

        # Create flags for testing (later) if "lat" and "lon" exist in 
        # this element. Default to False (i.e., doesn't exist). 
        lat_exists = False
        lon_exists = False

        # Create the "type" key/value in our dictionary for each type of tag.
        if element.tag == "node":
            node["type"] = "node"
        elif element.tag == "way":
            node["type"] = "way"

        # Iterate through each tag the current element   
        for tag in element.iter():
            # Iterate through each key in the current tag.attrib dictionary
            for key in tag.attrib.iterkeys():
                # Test if the current key is one that needs to be inserted
                # into the "created" dictionary, and if so, add it. 
                if key in CREATED:
                    if "created" not in node:
                        node["created"] = {}
                        node["created"].update([(key, tag.attrib[key])])
                    else:
                        node["created"].update([(key, tag.attrib[key])])
                # If the current key is "lat" or "lon", convert it to a 
                # float and update the applicable existence flags.
                elif key == "lat":
                    lat = float (tag.attrib[key])
                    lat_exists = True
                elif key =="lon":
                    lon = float (tag.attrib[key])
                    lon_exists = True
                elif key == "k":
                    # Omit the values for "k" and "v" if "k" contains a
                    # problem character.
                    if problemchars.search(tag.attrib[key]) is not None:
                        continue
                    # Add the values for "k" and "v" to the "address"
                    # dictionary if "k" starts with "addr:"
                    elif tag.attrib[key].startswith("addr:"):
                        # Omit the values for "k" and "v" if "k" contains
                        # a secondary street description.
                        if tag.attrib[key].count("street:") > 0:
                            continue
                        elif "address" not in node:
                            node["address"] = {}
                            node["address"].update([(tag.attrib[key].lstrip("addr:").strip(),tag.attrib["v"])])
                        else:
                            node["address"].update([(tag.attrib[key].lstrip("addr:").strip(),tag.attrib["v"])])
                    # If second level tag "k" value does not start with "addr:", 
                    # but contains ":", add to node dictionary.
                    elif ":" in key:
                        node.update([(tag.attrib[key], tag.attrib["v"])])

                # If the current element type is "way", add "ref" values 
                # to the "node_refs" dictionary.
                elif element.tag == "way" and key == "ref" :
                    if "node_refs" not in node:
                        node["node_refs"] = []
                        node["node_refs"].append(tag.attrib[key])
                    else:
                        node["node_refs"].append(tag.attrib[key]) 
                else:
                    node.update([(key, tag.attrib[key])])
        # If "lat" and "lon" values exist for this element, add them to the 
        # "pos" array. 
        if lat_exists and lon_exists:
            node["pos"] = [lat, lon]
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('example.osm', True)
    #pprint.pprint(data)
    
    correct_first_elem = {
        "id": "261114295", 
        "visible": "true", 
        "type": "node", 
        "pos": [41.9730791, -87.6866303], 
        "created": {
            "changeset": "11129782", 
            "user": "bbmiller", 
            "version": "7", 
            "uid": "451048", 
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.", 
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()