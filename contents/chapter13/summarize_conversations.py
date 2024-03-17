from common import client, model
import json
from retry import retry

system_role = """
당신은 사용자의 메시지를 아래의 JSON 형식으로 대화 내용을 주제별로 요약하는 기계입니다.
1. 주제는 구체적이며 의미가 있는 것이어야 합니다.
2. 요약 내용에는 '민지는...', '고비는...'처럼 대화자의 이름이 들어가야 합니다.
3. 원문을 최대한 유지하며 요약해야 합니다. 
4. 주제의 갯수는 무조건 5개를 넘지 말아야 하며 비슷한 내용은 하나로 묶어야 합니다.
```
{
    "data":
            [
                {"주제":<주제>, "요약":<요약>},
                {"주제":<주제>, "요약":<요약>},
            ]
}
"""

with open("대화원천내용.json", "r", encoding="utf-8") as f:
    conversations = json.load(f)

summaries = []

@retry(tries=5, delay=2)
def summarize(conversation):    
    try:
        conversation_str = json.dumps(conversation, ensure_ascii=False)
        message = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": conversation_str}
        ]
        response = client.chat.completions.create(
                    model=model.basic, 
                    messages=message,
                    temperature=0,
                    response_format={"type": "json_object"}
                ).model_dump()
        content = response['choices'][0]['message']['content']
        print(content)

        # JSON 로드
        summary = json.loads(content)
        summaries.append(summary["data"])
        
    except Exception as e:
        print("예외 발생, 재시도합니다.")
        raise e

for conversation in conversations:
    summarize(conversations)


# conversations 리스트를 JSON 파일로 저장
with open('대화내용요약.json', 'w', encoding='utf-8') as f:
    json.dump(summaries, f, ensure_ascii=False, indent=4)

