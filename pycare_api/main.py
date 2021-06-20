from fastapi import FastAPI
from pycare_api.data import query_data as qdata
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
        return qdata.updateHospitalDetailsData(), qdata.updateStatusData(), qdata.updateDistrictWiseReport()
    else:
        if updateOnly=="status":
            return qdata.updateStatusData()
        elif updateOnly=="hospitalDetails":
            return qdata.updateHospitalDetailsData() 


@app.get("/translation")
def translation():
    return qdata.getTranslation()


@app.get("/districtWiseReport")
def districtWiseReport():
    report = list(qdata.getData('districtWiseReport'))

    return report

