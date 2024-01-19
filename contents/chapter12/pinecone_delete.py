import os
import pinecone

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = "gcp-starter"

pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
index = pinecone.Index('jjinchin-memory')
index.delete(delete_all=True)