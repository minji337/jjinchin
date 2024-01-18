from tavily import TavilyClient
from pprint import pprint
tavily = TavilyClient(api_key=<복사한 API Key>) 
response = tavily.search(query="자율적 에이전트 요약", search_depth="advanced")
pprint(response)
