from pprint import pprint

import openai

# 여러분들이 발급받은 api_key로 바꿔주세요. 
api_key = "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"
client = openai.OpenAI(api_key=api_key)

model = "gpt-3.5-turbo-1106"

messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ]

response = client.chat.completions.create(model=model, messages=messages).model_dump()
pprint(response)
