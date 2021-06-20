import pymongo
import os
from pycare_api.data import scrape_data as sdata
from typing import Optional
from pymongo import MongoClient

db_username=os.environ.get('db_username')
db_pass=os.environ.get('db_pass')
url = "mongodb+srv://backend:sYPjEGvJzwPqFub3@pycare-api.xbmlx.mongodb.net/covid19Report?retryWrites=true&w=majority".format(db_username,db_pass)
client = pymongo.MongoClient(url.format(
    os.getenv("username"), os.getenv("password")))
db = client["covid19Report"]


def getData(collectionName: str, fields: Optional[list] = None):
    if fields != None:
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
                              "total": a["total"], "cured": a["cured"], "active": a["active"], "death": a["death"],"lastUpdatedOn":a["lastUpdatedOn"]}})
        return "successfully updated status collection", a
    except Exception as err:
        return str(err)+"failed to update data status collection"

def getTranslation():
    cursor = db.get_collection("translation").find({}, {"_id": False})
    cursor = list(cursor)
    data = {key: c[key] for c in cursor for key in c.keys()}
    return data

def updateDistrictWiseReport():
    collection = db["districtWiseReport"]
    try:
        for i in sdata.districtWiseReport():
            collection.update_many({"district": i.district},
                                   {"$set": {
                                        "reported": i.reported,
                                        "active": i.active,
                                        "cured": i.cured,
                                        "death": i.death,
                                   }})
        return "successfully updated districtWiseReport collection"
    except Exception as err:
        return str(err)+"failed to update data districtWiseReport collection"