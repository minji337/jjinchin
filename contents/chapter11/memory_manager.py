from pymongo import MongoClient
import os
from common import today

mongo_cluster = MongoClient(os.getenv("MONGO_CLUSTER_URI"))
mongo_chats_collection = mongo_cluster["jjinchin"]["chats"]

class MemoryManager:

    def save_chat(self, context):        
        messages = []
        for message in context:
            if message.get("saved", True): 
                continue
            messages.append({"date":today(), "role": message["role"], "content": message["content"]})
                        
        if len(messages) > 0:           
            mongo_chats_collection.insert_many(messages)

    def restore_chat(self, date=None):
        search_date = date if date is not None else today()        
        search_results = mongo_chats_collection.find({"date": search_date})
        restored_chat = [{"role": v['role'], "content": v['content'], "saved": True} for v in search_results]
        return restored_chat
