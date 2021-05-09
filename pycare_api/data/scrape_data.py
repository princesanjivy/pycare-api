from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel
from datetime import datetime

url = "https://covid19dashboard.py.gov.in/"
keys = ["hospitalName", "isolationBeds", "oxygenBeds", "ventilatorBeds"]
availability = []


class BedAvailabilityModel(BaseModel):
    hospitalName: str
    isolationBeds: dict
    oxygenBeds: dict
    ventilatorBeds: dict
    # lastUpdateOn: datetime


def bedAvailability():
    response = requests.get(url + "/BedAvailabilityDetails")
    soup = BeautifulSoup(response.text, "lxml")

    for body in soup.find_all("tbody"):
        for tr in body.find_all("tr"):
            values = []
            td = tr.find_all("td")

            values.append(td[0].text.strip())
            for e in range(2, (len(td)//2)+1):
                values.append(
                    {"alloted": td[e].text.strip(),
                     "vacant": td[e+1].text.strip()})

            dataModel = BedAvailabilityModel.parse_obj(dict(zip(keys, values)))
            availability.append(dataModel)

    # return availability

bedAvailability()