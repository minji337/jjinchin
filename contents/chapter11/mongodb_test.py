from pymongo import MongoClient
import os

#cluster=MongoClient("mongodb+srv://<id>:<password>@cluster0.ov3wpli.mongodb.net/?retryWrites=true&w=majority")
cluster=MongoClient(os.getenv("MONGO_CLUSTER_URI"))
db=cluster["jjinchin"]
collection = db["chats"]

my_friend = {
				"name": "고비", 
				"age": 26,
				"job": "대중음악 작곡가",
				"character": "당신은 진지한 것을 싫어하며, 항상 밝고 명랑한 성격임",
				"best friend" : {"name": "김민지",
				         "situations":["회사 생활에 의욕을 찾지 못하고 창업을 준비하고 있음", 
						               "매운 음식을 좋아함",
							           "가장 좋아하는 가수는 '아이유'"]
			            }
            }

collection.insert_one(my_friend)

for result in collection.find({}):
    print(result)
    