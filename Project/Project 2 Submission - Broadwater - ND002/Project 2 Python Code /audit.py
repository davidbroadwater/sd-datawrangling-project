"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "san_diego.osm.xml"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_prefix_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)

expected = ["Avenue", "Boulevard", "Broadway", "Circle", "Commons", "Court", "Cove", 
            "Drive", "Highway", "Impasse", "Lane", "Mews", "North", "Parkway", "Paseo", "Place", "Plaza",
            "Road", "Row", "South", "Square", "Street", "Terrace", "Trail", "Vista", "Way", "Walk"]

expected_prefix = [ "Camino", "Calle", "Plaza", "Via"
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


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    p = street_type_prefix_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    # print street_types.items()
    return street_types


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
                            name = name.replace(street_prefix, prefix[street_prefix])
                            update_name.counter += 1
                        # else:
                        #     print name
            else:
                name = name.replace(street_type, mapping[street_type])
                update_name.counter += 1
    return name


def test():

    update_name.counter = 0
    st_types = audit(OSMFILE)
    #pprint.pprint(dict(st_types).keys())
    #pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name)
            #print name, "=>", better_name

    print update_name.counter


if __name__ == '__main__':
    test()
