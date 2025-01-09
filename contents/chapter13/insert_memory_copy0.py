import os
from pymongo import MongoClient

mongo_cluster = MongoClient(os.getenv("MONGO_CLUSTER_URI"))
mongo_memory_collection = mongo_cluster["jjinchin"]["memory"]

mongo_memory_collection.delete_many({})

query = {"_id": 1}
newvalues = {"$set": {"date": "20241101", "keyword": "value1",  "summary" : "value2"}} 
mongo_memory_collection.update_one(query, newvalues, upsert=True)
