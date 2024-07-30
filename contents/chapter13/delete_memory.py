import os
from pymongo import MongoClient


mongo_cluster = MongoClient(os.getenv("MONGO_CLUSTER_URI"))
mongo_memory_collection = mongo_cluster["jjinchin"]["memory"]
mongo_chats_collection = mongo_cluster["jjinchin"]["chats"]

mongo_memory_collection.delete_many({})
for result in mongo_memory_collection.find({}):
    print(result)


mongo_chats_collection.delete_many({})
for result in mongo_chats_collection.find({}):
    print(result)


from pinecone.grpc import PineconeGRPC as Pinecone
from pymongo import MongoClient

pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pinecone.Index("jjinchin-memory")

pinecone_index.delete(delete_all=True)

print(pinecone_index.describe_index_stats())
