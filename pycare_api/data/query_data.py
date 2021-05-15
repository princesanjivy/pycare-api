import pymongo
import os
from typing import Optional
from pymongo import MongoClient

url = "mongodb+srv://backend:sYPjEGvJzwPqFub3@pycare-api.xbmlx.mongodb.net/covid19Report?retryWrites=true&w=majority"
client = pymongo.MongoClient(url.format(
    os.getenv("username"), os.getenv("password")))
db = client["covid19Report"]


def getData(collectionName: str, fields: Optional[list] = None):
    if fields != None:
        fields.append("hospitalName")
        showOnly = dict(zip(fields, [True]*len(fields)))
        showOnly["_id"] = False
        return db.get_collection(collectionName).find({}, showOnly)
    else:
        return db.get_collection(collectionName).find({}, {"_id": False})



