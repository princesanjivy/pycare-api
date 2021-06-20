from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel
import re

url = "https://covid19dashboard.py.gov.in/"

class HospitalDetailsModel(BaseModel):
    hospitalName: str
    isolationBeds: dict
    oxygenBeds: dict
    ventilatorBeds: dict
    lastUpdateOn: str

class DistrictWiseReport(BaseModel):
    district: str
    reported: str
    cured: str
    active: str
    death: str


def hospitalDetails():
    availability = []
    keys = ["hospitalName", "lastUpdateOn",
            "isolationBeds", "oxygenBeds", "ventilatorBeds"]
    response = requests.get(url + "/BedAvailabilityDetails")
    soup = BeautifulSoup(response.text, "lxml")
    for body in soup.find_all("tbody"):
        for tr in body.find_all("tr"):
            values = []
            td = tr.find_all("td")
            if len(td) != 1:
                values.append(td[0].text.strip())
                values.append(td[1].text.strip())
                for e in range(2, len(td), 2):
                    values.append(
                        {"vacant": int(td[e+1].text.strip()),
                        "alloted": int(td[e].text.strip())})
                dataModel = HospitalDetailsModel.parse_obj(
                    dict(zip(keys, values)))
                availability.append(dataModel)
    return availability

def extract_numb(text):
    reg = "(\d*)"
    match = re.match(reg, text)
    return match.group()

def status():
    report = []
    keys = ["total", "cured", "active", "death","lastUpdatedOn"]
    output = []
    response = requests.get(url + "/Home")
    soup = BeautifulSoup(response.text, "lxml")
    for body in soup.find_all("div",  class_="card-body"):
        if "Total Reported" in body.text:
            for i in body.text.split('\n'):
                if "Total Reported" in i:
                    output.append(extract_numb(i))
        if "Cured" in body.text:
            for i in body.text.split('\n'):
                if "Cured" in i:
                    output.append(extract_numb(i))
        if "Active" in body.text:
            for i in body.text.split('\n'):
                if "Active" in i:
                    output.append(extract_numb(i))
        if "Death" in body.text:
            for i in body.text.split('\n'):
                if "Death" in i:
                    output.append(extract_numb(i))
    for body in soup.find_all("footer"):
        if "Last" in body.text:
            output.append (body.text.strip().split("\n")[1].strip())

    report.append(dict(zip(keys, output)))

    return report
    
def districtWiseReport():
    keys = ["district", "reported", "cured", "active", "death"]
    response = requests.get(url + "/Reporting/District")
    soup = BeautifulSoup(response.text, "lxml")
    output = []

    tables = soup.find_all("tbody")
    tr = tables[1].find_all("tr")

    for trs in tr:
        d=[]
        for data in trs.find_all("td"):
            d.append(data.text.strip())
        # output.append(dict(zip(keys, d)))
        dataModel = DistrictWiseReport.parse_obj(
                    dict(zip(keys, d)))
        output.append(dataModel)

        
    return output