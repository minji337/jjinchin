import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

template = """
신조어에 대한 질문입니다. 아래 JSON 포맷으로 답하세요.
{"자만추": <30단어 이내로 뜻 설명>,
 "좋댓구알": <30단어 이내로 뜻 설명>,
 "어쩔티비": <30단어 이내로 뜻 설명>,
 "가심비": <30단어 이내로 뜻 설명>,
 "갓생": <30단어 이내로 뜻 설명>}
"""
context = [{"role": "user", "content": template}] 
response = client.chat.completions.create(
            model="gpt-3.5-turbo-0613", 
            messages=context,
            temperature=0,
            top_p=0
        ).model_dump()
print(response['choices'][0]['message']['content'])

system_role = """
신조어 사전:
{"자만추": "자연스러운 만남 추구"
 "좋댓구알": "좋아요, 댓글, 구독 알림설정의 줄임말",
 "어쩔티비": "어쩌라고 안 물어봤는데 를 뜻하는 말"
 "가심비": "가격 대비 심리적 만족도가 주는 효용"
 "갓생": "일상의 소소한 성취감을 추구하는 삶"}

신조어 사전에서 답하세요. 신조어 사전에 없다면 "모르는 단어입니다"라고 답하세요."""

template = """
신조어 {신조어}의 뜻을 말해주세요.
""".format(신조어="자만추")

context = [{"role": "system", "content": system_role},
           {"role": "user", "content": template}] 
response = client.chat.completions.create(
            model="gpt-3.5-turbo-0613", 
            messages=context,
            temperature=0,
            top_p=0
        ).model_dump()
print(response['choices'][0]['message']['content'])
