import fastapi
import scrape_data as data
from typing import Optional
import json
from pymongo import MongoClient

app = fastapi.FastAPI(title="PyCare", description="API for pycare", version="1.0.0")


client = MongoClient("mongodb+srv://backend:sYPjEGvJzwPqFub3@pycare-api.xbmlx.mongodb.net/covid19Report?retryWrites=true&w=majority")
db = client.test

db = client["covid19Report"]
Collection = db["bedAvailability"]

with open('bedAvailability.json') as file:
    file_data = json.load(file)


def updateData():
    for i in data.availability:
        Collection.update_many({"hospitalName": i.hospitalName}, {"$set":{"isolationBeds.alloted": i.isolationBeds['alloted'],"isolationBeds.vacant": i.isolationBeds['vacant'],"oxygenBeds.alloted": i.oxygenBeds['alloted'],"oxygenBeds.vacant": i.oxygenBeds['vacant'],"ventilatorBeds.alloted": i.ventilatorBeds['alloted'],"ventilatorBeds.vacant": i.ventilatorBeds['vacant']}})

@app.get("/bedAvailability",
         responses={
             200: {
                 "description": '''Lists the number of availabilities of beds.\n
                 Has optional query param "bedType" to get specific type of bed availability''',
                 "content": {
                     "application/json": {
                         "example": [{
                             "hospitalName": "PIMS",
                             "lastUpdateOn":"09-05-2021 08:52:50",
                             "isolationBeds": {
                                 "alloted": "80",
                                 "vacant": "3"
                             },
                             "oxygenBeds": {
                                 "alloted": "5",
                                 "vacant": "100"
                             },
                             "ventilatorBeds": {
                                 "alloted": "100",
                                 "vacant": "0"
                             }
                         }]
                     }
                 }
             }
         })

def bedAvailability(bedType: Optional[str] = None):
    if bedType == None:
        return data.availability
    else:
        return [{"hospitalName": i.hospitalName, bedType: getattr(i, bedType)} for i in data.availability]

updateData()