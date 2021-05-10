from fastapi import FastAPI
from typing import Optional
from data import query_data as db

app = FastAPI(title="PyCare", description="API for pycare", version="1.0.0")


# @app.get("/listHospitals",
#          responses={
#              200: {
#                  "description": "List of hospitals in Puducherry",
#                  "content": {
#                      "application/json": {
#                          "example": ["PIMS", "JIPMER"]
#                      }
#                  }
#              }
#          })
# def listHospitals():
#     return [i.hospitalName for i in data.availability]


# @app.get("/bedAvailability",
#          responses={
#              200: {
#                  "description": '''Lists the number of availabilities of beds.\n
#                  Has optional query param "bedType" to get specific type of bed availability''',
#                  "content": {
#                      "application/json": {
#                          "example": [{
#                              "hospitalName": "PIMS",
#                              "isolationBeds": {
#                                  "alloted": "80",
#                                  "vacant": "5"
#                              },
#                              "oxygenBeds": {
#                                  "alloted": "5",
#                                  "vacant": "100"
#                              },
#                              "ventilatorBeds": {
#                                  "alloted": "100",
#                                  "vacant": "0"
#                              }
#                          }]
#                      }
#                  }
#              }
#          })
# def bedAvailability(bedType: Optional[str] = None):
#     if bedType == None:
#         return data.availability
#     else:
#         return [{"hospitalName": i.hospitalName, bedType: getattr(i, bedType)} for i in data.availability]


# example for status
# make one for hospitalDetails

@app.get("/status")
def status():
    return db.getData("status")[0]


@app.get("/updateData")
def updateData(updateOnly: Optional[str] = None):
    # when query param is not passed in request header scrap and update both the collections
    # else update only the collection which is requested

    # write if part here
    return {"updation": db.updateData()}
