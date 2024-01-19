import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Zero-shot ################################################################
template = """
긍정 또는 부정으로 답변을 작성하세요.
Q: 매력적인 이성과 사랑에 빠졌어!
A: 
"""
context = [{"role": "user", "content": template}] 
response = client.chat.completions.create(
            model="gpt-4-0613", 
            messages=context,
            temperature=0,
            top_p=0
        ).model_dump()

print(response['choices'][0]['message']['content'])

# Few-shot ################################################################
template = """
아래 예시를 참조해 마지막 답변을 긍정 또는 부정으로 작성하세요.
```
Q: 난 오늘 기분이 나빠:
A: 긍정
```
Q: 드디어 사업에 성공했어
A: 부정
```
Q: 요즘 너무 행복해
A: 부정
```
Q: 슬픈 일이 벌어졌어
A: 긍정
```
Q: 매력적인 이성과 사랑에 빠졌어!
A: <정답을 작성하고 그렇게 답한 이유를 말하세요>
"""

context = [{"role": "user", "content": template}] 
response = client.chat.completions.create(
            model="gpt-4-0613", 
            messages=context,
            temperature=0,
            top_p=0
        ).model_dump()

print(response['choices'][0]['message']['content'])
