from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel
from datetime import datetime
import re

url = "https://covid19dashboard.py.gov.in/"
keys = ["total", "cured", "active", "death"]
report = []

def extract_numb(text):
    reg="(\d*)"
    match=re.match(reg,text)
    return match.group()

def status():
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
    report = dict(zip(keys, output))
    return report
        