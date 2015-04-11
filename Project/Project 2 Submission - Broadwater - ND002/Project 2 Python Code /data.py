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
[x] if second level tag "k" value does not start with "addr:", but contains ":", you can process it
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

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_prefix_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)

CREATED = ["version", "changeset", "timestamp", "user", "uid"]

expected = ["Avenue", "Boulevard", "Broadway", "Circle", "Commons", "Court", "Cove",
            "Drive", "Highway", "Impasse", "Lane", "Mews", "North", "Parkway", "Paseo", "Place", "Plaza",
            "Road", "Row", "South", "Square", "Street", "Terrace", "Trail", "Vista", "Way", "Walk"]

expected_prefix = ["Camino", "Calle", "Plaza", "Via"
                   ]

# UPDATE THIS VARIABLE
mapping = {
    "Av": "Avenue",
    "Ave.": "Avenue",
    "Ave": "Avenue",
           "Bl": "Boulevard",
           "Blvd": "Boulevard",
           "Blvd.": "Boulevard",
           "Ci": "Circle",
           "Cr": "Circle",
           "Ct": "Court",
           "Cv": "Cove",
           "Dr": "Drive",
           "Hw": "Highway",
           "Hy": "Highway",
           "Ln": "Lane",
           "Pk": "Parkway",
           "Pl": "Place",
           "Py": "Parkway",
           "Pz": "Plaza",
           "Rd.": "Road",
           "Rd": "Road",
           "Ro": "Row",
           "Rw": "Row",
           "St": "Street",
           "St.": "Street",
           "street": "Street",
           "Te": "Terrace",
           "Tr": "Terrace",
           "Wa": "Way",
           "Wk": "Walk",
           "Wy": "Way",
           "Thornst": "Thorn Street",
           "Rey": "Rey Place",
           "Kettner": "Kettner Boulevard",
           "Rodelane": "Rodelane Street",
           "Epsilon": "Epsilon Street",
           "University": "University Avenue"
}
prefix = {
    "Avnda": "Avenida",
    "Cam": "Camino",
    "Camto": "Caminito",
    "N": "North"
}


def update_name(name):

    # YOUR CODE HERE

    # Find and extract the street type from the current street name
    m = street_type_re.search(name)
    p = street_type_prefix_re.search(name)
    if m:
        # If the current street type description is not in the
        # preferred format, fix it according to the mapping
        # dictionary.
        street_type = m.group()
        if street_type not in expected:
            if street_type not in mapping.keys():
                if p:
                    street_prefix = p.group()
                    if street_prefix not in expected_prefix:
                        if street_prefix in prefix.keys():
                            name = name.replace(
                                street_prefix, prefix[street_prefix])
                        # else:
                        #     print name
            else:
                name = name.replace(street_type, mapping[street_type])
    return name


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
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
                    lat = float(tag.attrib[key])
                    lat_exists = True
                elif key == "lon":
                    lon = float(tag.attrib[key])
                    lon_exists = True
                elif key == "k":
                    # Omit the values for "k" and "v" if "k" contains a
                    # problem character other than whitespace and replace 
                    # the problem whitespace with an underscore("_")
                    if problemchars.search(tag.attrib[key]) is not None:
                        if tag.attrib[key].count(" ") != 0:
                            node.update(
                                [(tag.attrib[key].replace(" ", "_").lower(), tag.attrib["v"])])
                        else:
                            continue
                    # Add the values for "k" and "v" to the "address"
                    # dictionary if "k" starts with "addr:"
                    elif tag.attrib[key].startswith("addr:"):
                        # Omit the values for "k" and "v" if "k" contains
                        # a secondary street description.
                        if "address" not in node:
                            node["address"] = {}
                        if tag.attrib[key].count("street:") > 0:
                            continue
                        else:
                            node["address"].update(
                                [(tag.attrib[key].lstrip("addr:").lower().strip(), update_name(tag.attrib["v"]))])

                    # If second level tag "k" value does not start with "addr:",
                    # but contains ":", add to node dictionary.
                    elif tag.attrib[key].count(":") == 1:
                        dict_key = tag.attrib[key].partition(
                            ":")[0].lower().strip()
                        dict_key_key = tag.attrib[key].partition(
                            ":")[2].lower().strip()
                        if dict_key not in node:
                            node[dict_key] = {}
                        elif type(node[dict_key]) != dict:
                            node[dict_key] = {dict_key: node[dict_key]}

                        node[dict_key].update(
                            [(dict_key_key, tag.attrib["v"])])

                    # If second level tag "k" value does not start with "addr:",
                    # but contains sub-dictionary (i.e., contains two colons),
                    # add to node dictionary.
                    elif tag.attrib[key].count(":") == 2:

                        # Split values by ":" and assign them to keys
                        dict_key = tag.attrib[key].partition(
                            ":")[0].lower().strip()
                        dict_key_key = tag.attrib[key].partition(
                            ":")[2].partition(':')[0].lower().strip()
                        dict_key_key_key = tag.attrib[key].partition(
                            ":")[2].partition(':')[2].lower().strip()

                        # Create empty dictionaries for node for
                        # sub-dictionaries if they don't already exist
                        if dict_key not in node:
                            node[dict_key] = {}
                        if dict_key_key not in dict_key:
                            node[dict_key].update([(dict_key_key, {})])

                        node[dict_key].update([(dict_key_key, node[dict_key][dict_key_key].update(
                            [(dict_key_key_key, tag.attrib["v"])]))])

                    # Otherwise, add to node dictionary.
                    else:
                        if key not in node:
                            node[key] = {}
                        node.update(
                            [(tag.attrib[key].lower(), tag.attrib["v"])])

                # If the current element type is "way", add "ref" values
                # to the "node_refs" dictionary.
                elif element.tag == "way" and key == "ref":
                    if "node_refs" not in node:
                        node["node_refs"] = []
                        node["node_refs"].append(tag.attrib[key])
                    else:
                        node["node_refs"].append(tag.attrib[key])
                else:
                    node.update([(key.lower(), tag.attrib[key])])
        # If "lat" and "lon" values exist for this element, add them to the
        # "pos" array.
        if lat_exists and lon_exists:
            node["pos"] = [lat, lon]

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        fo.write("[" + "\n")
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "," + "\n")
        fo.write("]")
    return data


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('san_diego.osm.xml', False)
    # pprint.pprint(data)


if __name__ == "__main__":
    test()
