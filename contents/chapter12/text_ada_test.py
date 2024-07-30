from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

message = "신데렐라와 왕자는 사랑에 빠졌습니다."
result = client.embeddings.create(input=message, model="text-embedding-ada-002").model_dump()
print(result)