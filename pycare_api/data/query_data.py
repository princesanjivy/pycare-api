import pymongo
import os
from typing import Optional

url = 'mongodb+srv://{}:{}@pycare-api.xbmlx.mongodb.net/covid19Report?retryWrites=true&w=majority'
client = pymongo.MongoClient(url.format(
    os.getenv("username"), os.getenv("password")))

db = client["covid19Report"]


def getData(collectionName: str,
            fields: Optional[list] = None):
    if fields != None:
        showOnly = dict(zip(fields, [True]*len(fields)))
        showOnly["_id"] = False
        
        return db.get_collection(collectionName).find({}, showOnly)
    else:
        print("all")

        return db.get_collection(collectionName).find({}, {"_id":False})

# def putData(collectionName, data):
    # collection = db.get_collection(collectionName)

# print(getData("status", fields=["total", "death"])[0])
