import os
from pinecone.grpc import PineconeGRPC as Pinecone

pinecone_api_key = os.getenv("PINECONE_API_KEY")

pinecone = Pinecone(api_key=pinecone_api_key)
index = pinecone.Index('jjinchin-memory')
index.delete(delete_all=True)