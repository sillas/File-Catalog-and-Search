import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["file_catalog"]
collection = db["files"]
