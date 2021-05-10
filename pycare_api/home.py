from fastapi import FastAPI
import home_data as data
from typing import Optional

app = FastAPI(title="PyCare", description="API for pycare", version="1.0.0")


@app.get("/status",
         responses={
             200: {
                 "description": "Covid status in Pondicherry",
                 "content": {
                     "application/json": {
                         "example": [{
                             "total": "70076",
                             "cured":"55552",
                              "active":"13585",
                               "death":"939"
                             }]
                     }
                 }
             }
         })

def status():
    a=data.status()
    return a

status()
