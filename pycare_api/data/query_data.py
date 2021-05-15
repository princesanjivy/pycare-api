import pymongo
import os
from pycare_api.data import scrape_data as sdata
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

def updateHospitalDetailsData():
    collection = db["hospitalDetails"]
    try:
        for i in sdata.hospitalDetails():
            collection.update_many({"hospitalName": i.hospitalName},
                                   {"$set": {"isolationBeds.alloted": i.isolationBeds['alloted'],
                                             "isolationBeds.vacant": i.isolationBeds['vacant'],
                                             "oxygenBeds.alloted": i.oxygenBeds['alloted'],
                                             "oxygenBeds.vacant": i.oxygenBeds['vacant'],
                                             "ventilatorBeds.alloted": i.ventilatorBeds['alloted'],
                                             "ventilatorBeds.vacant": i.ventilatorBeds['vacant']}})
        return "successfully updated hospitalDetails collection"
    except Exception as err:
        return str(err)+"failed to update data hospitalDetails collection"

def updateStatusData():
    collection = db["status"]
    a = sdata.status()[0]
    try:
        collection.update_one({}, {"$set": {
                              "total": a["total"], "cured": a["cured"], "active": a["active"], "death": a["death"]}})
        return "successfully updated status collection"
    except Exception as err:
        return str(err)+"failed to update data status collection"



