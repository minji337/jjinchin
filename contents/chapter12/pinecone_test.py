from openai import OpenAI
import os
import pinecone
import time

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = "gcp-starter"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
index = pinecone.Index('jjinchin-memory')

text1 = """
신데렐라는 어려서 부모를 잃고 불친절한 새어머니와 언니들과 삽니다. 요정 대모님이 나타나 해주신 마법으로 왕자님의 무도회에 참석합니다. 밤 12시가 되면 마법이 풀린다는 조건 하에 왕자님과 춤을 추고, 서둘러 도망치면서 유리구두 하나를 잃습니다. 왕자님은 유리구두를 가지고 신데렐라를 찾아 결혼하게 됩니다.
"""
text2 = """
컴퓨터 구조는 CPU, 메모리, 입출력 장치 등으로 구성되며, 이들은 버스로 연결됩니다. CPU는 명령어를 실행하고, 메모리는 데이터와 프로그램을 저장합니다. 입출력 장치는 사용자와 시스템 간의 상호작용을 담당합니다. 이 구성요소들은 소프트웨어와 하드웨어의 효율적인 동작을 위해 설계되었습니다.
"""

vector1 = client.embeddings.create(input=text1, model="text-embedding-ada-002").data[0].embedding
vector2 = client.embeddings.create(input=text2, model="text-embedding-ada-002").data[0].embedding

index.upsert([("id1", vector1, {"input_date": "20230801"})])
index.upsert([("id2", vector2, {"input_date": "20230801"})])

time.sleep(10)

query = "동화책"
query_vector = client.embeddings.create(input=query, model="text-embedding-ada-002").data[0].embedding

search_response = index.query(filter={"input_date": "20230801"}, top_k=2, vector=query_vector)
print("search_response:", search_response)
