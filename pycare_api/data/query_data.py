import pymongo
import os
from typing import Optional
import scrape_data as data

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

        return db.get_collection(collectionName).find({}, {"_id": False})


def updateData():
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

