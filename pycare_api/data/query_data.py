import pymongo
import os
from typing import Optional
import scrape_data as data

import json
from pymongo import MongoClient


url = "mongodb+srv://backend:sYPjEGvJzwPqFub3@pycare-api.xbmlx.mongodb.net/covid19Report?retryWrites=true&w=majority"

client = pymongo.MongoClient(url.format(
    os.getenv("backend1"), os.getenv("sYPjEGvJzwPqFub3")))

db = client["covid19Report"]


def getData(collectionName: str, fields: Optional[list] = None):
    if fields != None:
        showOnly = dict(zip(fields, [True]*len(fields)))
        showOnly["_id"] = False
        return db.get_collection(collectionName).find({}, showOnly)
    else:
        print("all")
        return db.get_collection(collectionName).find({}, {"_id": False})

# a=getData('status',['total','cured'])
# for i in a: print(i)

def updatehospitaldetailsData():
    collection = db["bedAvailability"]
    try:
        for i in data.availability:
            collection.update_many({"hospitalName": i.hospitalName},
                                {"$set": {"isolationBeds.alloted": i.isolationBeds['alloted'],
                                            "isolationBeds.vacant": i.isolationBeds['vacant'],
                                            "oxygenBeds.alloted": i.oxygenBeds['alloted'],
                                            "oxygenBeds.vacant": i.oxygenBeds['vacant'],
                                            "ventilatorBeds.alloted": i.ventilatorBeds['alloted'],
                                            "ventilatorBeds.vacant": i.ventilatorBeds['vacant']}})

        return "successfully updated"
    except:
        return "failed to update data"

def updatestatusData():
    collection = db["status"]
    a=data.status()[0]
    try:
        collection.update_one({},{"$set":{"total":a["total"],"cured":a["cured"],"active":a["active"],"death":a["death"]}})
        return "successfully updated"
    except:
        return "failed to update data"


