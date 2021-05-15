from fastapi import FastAPI
from pycare_api.data import query_data as qdata
from pycare_api.data import scrape_data as sdata
from typing import Optional
import os
import pymongo

url = "mongodb+srv://backend:sYPjEGvJzwPqFub3@pycare-api.xbmlx.mongodb.net/covid19Report?retryWrites=true&w=majority"
client = pymongo.MongoClient(url.format(
    os.getenv("username"), os.getenv("password")))
db = client["covid19Report"]

app = FastAPI(
    title="PyCare", description="API for pycare", version="1.0.0")

@app.get("/hospitalDetails")
def hospitalDetails(fields: Optional[str] = None, sort: Optional[str] = None):
    if fields == None and sort == None:
        availability = list(qdata.getData('hospitalDetails'))
    elif fields != None and sort == None:
        availability = list(qdata.getData(
            "hospitalDetails", fields=fields.split(',')))
    elif sort != None and fields == None:
        availability = list(qdata.getData("hospitalDetails").sort(sort,-1))
    else:
        availability = list(qdata.getData("hospitalDetails", fields=fields.split(',')).sort(sort,-1))
    return availability


@app.get("/status")
def status(fields: Optional[str] = None):
    if fields == None:
        report = list(qdata.getData('status'))   # to get status
    else:
        report = list(qdata.getData("status", fields=fields.split(',')))
    return report

@app.get("/updateData")
def updateData(updateOnly: Optional[str] = None):
    if updateOnly == None:
        return updateHospitalDetailsData(), updateStatusData()
    else:
        if updateOnly=="status":
            return updateStatusData()
        elif updateOnly=="hospitalDetails":
            return updateHospitalDetailsData() 

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
        return "successfully updated hospitalDetails"
    except:
        return "failed to update data hospitalDetails"


def updateStatusData():
    collection = db["status"]
    a = sdata.status()[0]
    try:
        collection.update_one({}, {"$set": {
                              "total": a["total"], "cured": a["cured"], "active": a["active"], "death": a["death"]}})
        return "successfully updated status"
    except:
        return "failed to update data status"
