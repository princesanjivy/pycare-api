from fastapi import FastAPI
from data import query_data as data
from typing import Optional

app = FastAPI(
    title="PyCare", description="API for pycare", version="1.0.0")


@app.get("/hospitalDetails")
def hospitalDetails(fields: Optional[str] = None, sort: Optional[str] = None):
    if fields == None and sort == None:
        availability = list(data.getData('hospitalDetails'))
    elif fields != None and sort == None:
        availability = list(data.getData(
            "hospitalDetails", fields=fields.split(',')))
    elif sort != None and fields == None:
        availability = list(data.getData("hospitalDetails").sort(sort,-1))
    else:
        availability = list(data.getData("hospitalDetails", fields=fields.split(',')).sort(sort,-1))

    return availability


@app.get("/status")
def status(fields: Optional[str] = None):
    if fields == None:
        report = list(data.getData('status'))   # to get status
    else:
        # to get specific status
        report = list(data.getData("status", fields=fields.split(',')))
    return report
