from fastapi import FastAPI
import data.query_data as qdata
from typing import Optional

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
        return qdata.updateHospitalDetailsData(), qdata.updateStatusData()
    else:
        if updateOnly=="status":
            return qdata.updateStatusData()
        elif updateOnly=="hospitalDetails":
            return qdata.updateHospitalDetailsData() 

<<<<<<< HEAD
status()
=======

@app.get("/translation")
def translation():
    return qdata.getTranslation()
>>>>>>> ff82f8ada10e96409f3d10676784fc128350a71a
