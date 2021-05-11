from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel
from datetime import datetime
import re

url = "https://covid19dashboard.py.gov.in/"
availability = []

class BedAvailabilityModel(BaseModel):
    hospitalName: str
    isolationBeds: dict
    oxygenBeds: dict
    ventilatorBeds: dict
    lastUpdateOn: str

def bedAvailability():
    keys = ["hospitalName", "lastUpdateOn", "isolationBeds", "oxygenBeds", "ventilatorBeds"]
    response = requests.get(url + "/BedAvailabilityDetails")
    soup = BeautifulSoup(response.text, "lxml")
    for body in soup.find_all("tbody"):
        for tr in body.find_all("tr"):
            values = []
            td = tr.find_all("td")
            if len(td)!=1:
                values.append(td[0].text.strip())
                values.append(td[1].text.strip())
                for e in range(2, len(td), 2):
                    values.append(
                        {"alloted": td[e].text.strip(),
                        "vacant": td[e+1].text.strip()})
                dataModel = BedAvailabilityModel.parse_obj(dict(zip(keys, values)))
                availability.append(dataModel)


bedAvailability()

def extract_numb(text):
    reg="(\d*)"
    match=re.match(reg,text)
    return match.group()

def status():
    report = []
    keys = ["total", "cured", "active", "death"]
    output=[]
    response = requests.get(url + "/Home")
    soup = BeautifulSoup(response.text, "lxml")
    for body in soup.find_all("div",  class_ = "card-body"):
        if "Total Reported" in body.text:
            output.append(extract_numb(body.text))
        if "Cured" in body.text:
            output.append(extract_numb(body.text))
        if "Active" in body.text:
            output.append(extract_numb(body.text))
        if "Death" in body.text:
            output.append(extract_numb(body.text))
    report.append(dict(zip(keys, output)))
    return report

