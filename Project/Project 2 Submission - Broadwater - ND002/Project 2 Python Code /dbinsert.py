import json


def insert_data(data, db):

    for item in data:
        db.sd.insert(item)


if __name__ == "__main__":

    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.osm

    with open('san_diego.osm.xml.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
