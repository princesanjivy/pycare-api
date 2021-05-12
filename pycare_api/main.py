import fastapi
from data import query_data as data
from typing import Optional
import json
from pymongo import MongoClient

app = fastapi.FastAPI(
    title="PyCare", description="API for pycare", version="1.0.0")


@app.get("/hospitalDetails",
         responses={
             200: {
                 "description": '''Lists the number of availabilities of beds.\n
                 Has optional query param "bedType" to get specific type of bed availability''',
                 "content": {
                     "application/json": {
                         "example": [{
                             "hospitalName": "PIMS",
                             "lastUpdateOn": "09-05-2021 08:52:50",
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
def hospitalDetails(bedType: Optional[str] = None):
    availability = list(data.getData('hospitalDetails'))
    if bedType == None:
        return availability
    else:
        return [{"hospitalName": i.hospitalName, bedType: getattr(i, bedType)} for i in availability]

# endpoint for status


@app.get("/status",
         responses={
             200: {
                 "description": "Covid status in Pondicherry",
                 "content": {
                     "application/json": {
                         "example": [{
                             "total": "70076",
                             "cured": "55552",
                             "active": "13585",
                             "death": "939"
                         }]
                     }
                 }
             }
         })
def status(fields: Optional[str] = None):
    if fields == None:
        report = list(data.getData('status'))   # to get status
    else:
        report = list(data.getData("status", fields=fields.split(',')))     # to get specific status

    return report
