from pprint import pprint
import os
from openai import OpenAI

# 여러분들이 발급받은 api_key로 바꿔 주세요. 
# api_key = "sk-"
api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI() # 이것도 가능
client = OpenAI(api_key=api_key)

model = "gpt-4o-mini-2024-07-18"

messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ]

response = client.chat.completions.create(model=model, messages=messages).model_dump()
pprint(response)