# The size of the file:
db.sd.stats()
{
	"ns" : "osm.sd",
	"count" : 223768,
	"size" : 118657488,
	"avgObjSize" : 530,
	"storageSize" : 123936768,
	"numExtents" : 11,
	"nindexes" : 1,
	"lastExtentSize" : 37625856,
	"paddingFactor" : 1,
	"systemFlags" : 1,
	"userFlags" : 1,
	"totalIndexSize" : 7276640,
	"indexSizes" : {
		"_id_" : 7276640
	},
	"ok" : 1
}

# Number of unique users:
db.sd.distinct('created.user').length
339

# Number of posts with a user listed
db.sd.find({"created.user": {"$exists": "True"}}).count()
223768

db.sd.find({"address.postcode": {"$exists": "True"}}).count()

# Top Contributors:
db.sd.aggregate([{"$match": {"created.user": {"$exists": "True"}}},
                 {"$group": {"_id": "$created.user",
                             "count": {"$sum": 1}}},
                 {"$project": {"_id": 1, "count": 1,
                               "percentage": {"$divide": ["$count", 223768]}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 5}])

{ "_id" : "Adam Geitgey", "count" : 123451, "percentage" : 0.5516919309284616 }
{ "_id" : "Sat", "count" : 20176, "percentage" : 0.09016481355689822 }
{ "_id" : "woodpeck_fixbot", "count" : 15644, "percentage" : 0.06991169425476386 }
{ "_id" : "javbw", "count" : 11608, "percentage" : 0.05187515641199814 }
{ "_id" : "evil saltine", "count" : 7042, "percentage" : 0.03147009402595546 }

# Zip Codes listed:
db.sd.aggregate([{"$match": {"address.postcode": {"$exists": "True"}}},
                 {"$group": {"_id": "$address.postcode",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "92105", "count" : 10136 } # San Diego
{ "_id" : "92104", "count" : 8446 } # San Diego
{ "_id" : "92113", "count" : 7222 } # San Diego
{ "_id" : "92116", "count" : 6662 } # San Diego
{ "_id" : "92102", "count" : 6498 } # San Diego
{ "_id" : "92103", "count" : 6363 } # San Diego
{ "_id" : "92115", "count" : 4831 } # San Diego
{ "_id" : "92114", "count" : 4004 } # San Diego
{ "_id" : "91950", "count" : 3709 } # San Diego
{ "_id" : "92118", "count" : 3476 } # Coronado
{ "_id" : "92101", "count" : 2062 } # San Diego
{ "_id" : "92110", "count" : 1352 } # San Diego
{ "_id" : "92111", "count" : 847 } # San Diego
{ "_id" : "92139", "count" : 321 } # San Diego
{ "_id" : "92108", "count" : 288 } # San Diego
{ "_id" : "92136", "count" : 77 } # San Diego
{ "_id" : "92135", "count" : 26 } # San Diego / NAS North Island
{ "_id" : "CA 92101", "count" : 18 } # San Diego
{ "_id" : "92154", "count" : 4 } # San Diego
{ "_id" : "92140", "count" : 4 } # San Diego
{ "_id" : "92182", "count" : 3 } # San Diego
{ "_id" : "92100", "count" : 3 } # NOT VALID ZIPCODE
{ "_id" : "92103-3609", "count" : 2 }  # San Diego
{ "_id" : "92102-4810", "count" : 1 } # San Diego
{ "_id" : "92110-9998", "count" : 1 } # San Diego
{ "_id" : "91932", "count" : 1 } # Imperial Beach
{ "_id" : "92037", "count" : 1 } #La Jolla
{ "_id" : "92103-3607", "count" : 1 }  # San Diego
{ "_id" : "92024", "count" : 1 } # Encinitas
{ "_id" : "92020", "count" : 1 } # El Cajon
{ "_id" : "92108-3803", "count" : 1 }  # San Diego
{ "_id" : "CA 92101-6144", "count" : 1 }  # San Diego
{ "_id" : "92137", "count" : 1 }  # San Diego

# Cities listed for Invalid Zip Code
db.sd.aggregate([{"$match": {"address.postcode": "92100"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "San Diego", "count" : 3 }

# Cities listed for Imperial Beach Zip Code
db.sd.aggregate([{"$match": {"address.postcode": "91932"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "San Diego", "count" : 1 }

# Cities listed for La Jolla Zip Code
db.sd.aggregate([{"$match": {"address.postcode": "92037"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "San Diego", "count" : 1 }

# Cities listed for Encinitas Zip Code
db.sd.aggregate([{"$match": {"address.postcode": "92024"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "Encinitas", "count" : 1 }

# Cities listed for El Cajon Zip Code
db.sd.aggregate([{"$match": {"address.postcode": "92020"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "San Diego", "count" : 1 }

# Cities Listed

db.sd.aggregate([{"$match": {"address.city": {"$exists": "True"}}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "San Diego", "count" : 59074 }
{ "_id" : "National City", "count" : 3734 }
{ "_id" : "Coronado", "count" : 3492 }
{ "_id" : "Encinitas", "count" : 1 }


# Zip Codes listed for National City:
db.sd.aggregate([{"$match": {"address.city": "National City"}},
                 {"$group": {"_id": "$address.postcode",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "91950", "count" : 3704 }
{ "_id" : "92114", "count" : 30 }

# Cities listed for National City Zip Code
db.sd.aggregate([{"$match": {"address.postcode": "91950"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "National City", "count" : 3704 }
{ "_id" : "San Diego", "count" : 5 }

# Zip Code Incorrectly Marked as National City
db.sd.aggregate([{"$match": {"address.postcode": "92114"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "San Diego", "count" : 3974 }
{ "_id" : "National City", "count" : 30 }

# Zip Codes listed for Coronado:
db.sd.aggregate([{"$match": {"address.city": "Coronado"}},
                 {"$group": {"_id": "$address.postcode",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "92118", "count" : 3466 }
{ "_id" : "92135", "count" : 26 }

# Cities listed for Coronado Zip Code
db.sd.aggregate([{"$match": {"address.postcode": "92118"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "Coronado", "count" : 3466 }
{ "_id" : null, "count" : 10 }

# Cities listes for NAS North Island Zip Code
db.sd.aggregate([{"$match": {"address.postcode": "92135"}},
                 {"$group": {"_id": "$address.city",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}])

{ "_id" : "Coronado", "count" : 26 }

# Most popular type of Amenity:
db.sd.aggregate([{"$match": {"amenity": {"$exists": "True"}}},
                 {"$group": {"_id": "$amenity",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 20}])

{ "_id" : "place_of_worship", "count" : 364 }
{ "_id" : "parking", "count" : 339 }
{ "_id" : "restaurant", "count" : 152 }
{ "_id" : "school", "count" : 149 }
{ "_id" : "fast_food", "count" : 115 }
{ "_id" : "bar", "count" : 99 }
{ "_id" : "cafe", "count" : 40 }
{ "_id" : "fuel", "count" : 27 }
{ "_id" : "bench", "count" : 24 }
{ "_id" : "toilets", "count" : 23 }
{ "_id" : "drinking_water", "count" : 21 }
{ "_id" : "library", "count" : 21 }
{ "_id" : "bank", "count" : 20 }
{ "_id" : "parking_entrance", "count" : 20 }
{ "_id" : "hospital", "count" : 20 }
{ "_id" : "post_box", "count" : 16 }
{ "_id" : "atm", "count" : 16 }
{ "_id" : "post_office", "count" : 14 }
{ "_id" : "theatre", "count" : 13 }
{ "_id" : "fountain", "count" : 12 }

# Most popular type of Cuisine:
db.sd.aggregate([{"$match": {"cuisine": {"$exists": "True"}}},
                 {"$group": {"_id": "$cuisine",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 10}])

{ "_id" : "burger", "count" : 39 }
{ "_id" : "mexican", "count" : 28 }
{ "_id" : "sandwich", "count" : 23 }
{ "_id" : "pizza", "count" : 16 }
{ "_id" : "coffee_shop", "count" : 13 }
{ "_id" : "american", "count" : 11 }
{ "_id" : "sushi", "count" : 5 }
{ "_id" : "thai", "count" : 4 }
{ "_id" : "italian", "count" : 4 }
{ "_id" : "chinese", "count" : 4 

# Most popular Fast Food Cuisine:
db.sd.aggregate([{"$match": {"cuisine": {"$exists": "True"},
                             "amenity": "fast_food"}},
                 {"$group": {"_id": "$cuisine",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 10}])

{ "_id" : "burger", "count" : 36 }
{ "_id" : "sandwich", "count" : 20 }
{ "_id" : "mexican", "count" : 12 }
{ "_id" : "pizza", "count" : 11 }
{ "_id" : "chicken", "count" : 3 }
{ "_id" : "ice_cream", "count" : 2 }
{ "_id" : "bagel", "count" : 2 }
{ "_id" : "american", "count" : 2 }
{ "_id" : "chinese", "count" : 2 }
{ "_id" : "burgers_etc", "count" : 1 }

# Most popular name of Fast Food:
db.sd.aggregate([{"$match": {"name": {"$exists": "True"},
                             "amenity": "fast_food"}},
                 {"$group": {"_id": "$name",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 20}])

{ "_id" : "Jack in the Box", "count" : 16 }
{ "_id" : "Subway Sandwiches", "count" : 13 }
{ "_id" : "McDonald's", "count" : 9 }
{ "_id" : "Carls Jr.", "count" : 5 }
{ "_id" : "Dominos Pizza", "count" : 4 }
{ "_id" : "Taco Bell", "count" : 4 }
{ "_id" : "Wendy's", "count" : 3 }
{ "_id" : "Papa Johns", "count" : 3 }
{ "_id" : "Burger King", "count" : 3 }
{ "_id" : "Panda Express", "count" : 3 }
{ "_id" : "KFC", "count" : 3 }
{ "_id" : "Del Taco", "count" : 3 }
{ "_id" : "Subway", "count" : 3 }
{ "_id" : "Quiznos Subs", "count" : 2 }
{ "_id" : "Bruegger's Bagels", "count" : 2 }
{ "_id" : "Rubio's Baja Grill", "count" : 2 }
{ "_id" : "Wetzel's Pretzels", "count" : 2 }
{ "_id" : "Cotijas", "count" : 1 }
{ "_id" : "Cold Stone Creamery", "count" : 1 }
{ "_id" : "Dairy Queen", "count" : 1 }

# Most popular Restaurant Cuisine:
db.sd.aggregate([{"$match": {"cuisine": {"$exists": "True"},
                             "amenity": "restaurant"}},
                 {"$group": {"_id": "$cuisine",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 10}])

{ "_id" : "mexican", "count" : 15 }
{ "_id" : "american", "count" : 8 }
{ "_id" : "pizza", "count" : 5 }
{ "_id" : "sushi", "count" : 5 }
{ "_id" : "italian", "count" : 4 }
{ "_id" : "thai", "count" : 4 }
{ "_id" : "burger", "count" : 3 }
{ "_id" : "steak_house", "count" : 3 }
{ "_id" : "deli", "count" : 2 }
{ "_id" : "sandwich", "count" : 2 }

# Most popular name of Restaurant:
db.sd.aggregate([{"$match": {"name": {"$exists": "True"},
                             "amenity": "restaurant"}},
                 {"$group": {"_id": "$name",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 5}])

{ "_id" : "Crazee Burger", "count" : 2 }
{ "_id" : "Moncai Vegan", "count" : 1 }
{ "_id" : "Joe's Crab Shack", "count" : 1 }
{ "_id" : "Ruby's Diner", "count" : 1 }
{ "_id" : "Arrivederci", "count" : 1 }

# Most popular name of Cafe:
db.sd.aggregate([{"$match": {"name": {"$exists": "True"},
                             "amenity": "cafe"}},
                 {"$group": {"_id": "$name",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 5}])

{ "_id" : "Starbucks", "count" : 6 }
{ "_id" : "Starbucks Coffee", "count" : 5 }
{ "_id" : "Peet's Coffee & Tea", "count" : 2 }
{ "_id" : "Aromas", "count" : 1 }
{ "_id" : "JJ's Sunset Deli by the Bayside", "count" : 1 }

# Most popular type of religion:
db.sd.aggregate([{"$match": {"religion": {"$exists": "True"},
                             "amenity": "place_of_worship"}},
                 {"$group": {"_id": "$religion",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 5}])

{ "_id" : "christian", "count" : 324 }
{ "_id" : "buddhist", "count" : 4 }
{ "_id" : "muslim", "count" : 3 }
{ "_id" : "hindu", "count" : 2 }
{ "_id" : "bahai", "count" : 1 }
{ "_id" : "scientologist", "count" : 1 }
{ "_id" : "taoist", "count" : 1 }
{ "_id" : "ascended_master_teachings", "count" : 1 }
{ "_id" : "jewish", "count" : 1 }
{ "_id" : "unitarian", "count" : 1 }

# Most popular religious denomination:
db.sd.aggregate([{"$match": {"denomination": {"$exists": "True"},
                             "amenity": "place_of_worship"}},
                 {"$group": {"_id": "$denomination",
                             "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": 10}])

{ "_id" : "baptist", "count" : 50 }
{ "_id" : "catholic", "count" : 16 }
{ "_id" : "methodist", "count" : 13 }
{ "_id" : "lutheran", "count" : 10 }
{ "_id" : "presbyterian", "count" : 9 }
{ "_id" : "anglican", "count" : 7 }
{ "_id" : "seventh_day_adventist", "count" : 7 }
{ "_id" : "pentecostal", "count" : 7 }
{ "_id" : "jehovahs_witness", "count" : 7 }
{ "_id" : "orthodox", "count" : 3 }

# Number of Nodes:
db.sd.find({"type": "node"}).count()

207348

# Number of Ways:
db.sd.find({"type": "way"}).count()

16410
