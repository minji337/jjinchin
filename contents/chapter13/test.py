
from pymongo import MongoClient
import os
from pinecone.grpc import PineconeGRPC as Pinecone

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone = Pinecone(api_key=pinecone_api_key)
pinecone_index = pinecone.Index("jjinchin-memory")

mongo_cluster = MongoClient(os.getenv("MONGO_CLUSTER_URI"))
mongo_chats_collection = mongo_cluster["jjinchin"]["chats"]
mongo_memory_collection = mongo_cluster["jjinchin"]["memory"]
embedding_model = "text-embedding-ada-002"

date='20230804' # 이 일자의 벡터 DB, Mongo DB 삭제

search_results = mongo_memory_collection.find({"date": date})
#pinecone_index.delete(filter={"date":date})
ids = [ str(v['_id']) for v in search_results]
print(ids)
print(list(iter(search_results)))


if len(ids) > 0:
    pinecone_index.delete(ids=ids)
    mongo_memory_collection.delete_many({"date":date})
    mongo_chats_collection.delete_many({"date":date})