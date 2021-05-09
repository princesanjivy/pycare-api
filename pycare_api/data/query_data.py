import pymongo

url = 'mongodb+srv://princesanjivy:dnoLwh2MYLHwQS2W@snow-princebot.lgc4v.mongodb.net/test_pycare_api?retryWrites=true&w=majority'
client = pymongo.MongoClient(url)

db = client["test_pycare_api"]

collection = db.get_collection("listHospitals")

for doc in collection.find():
    print(doc)
