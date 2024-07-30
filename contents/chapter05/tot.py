import openai
import os
import json

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 프롬프트 ################################################################

agenda = """
'인공지능이 인간의 일자리를 위협합니다. 이에 대한 대응 방안을 논의합니다.'
"""

sampling_tempalte = """
{agenda}에 대해 논의 중입니다.
```
[이전 의견]:
{selected}
```
[이전 의견]에 대한 구체적이며 실질적인 구현 방안을 아래 JSON 형식으로 답하세요.
{{
    "주제": <주제>
    "구현": <50단어 이내로 작성하세요>,
    "근거": <[이전 의견]의 어떤 대목에서 그렇게 생각했는지>
 }}
"""

evaluation_template = """
{agenda}에 대해 논의하고 있습니다.
```
[의견]: 
{thought}
```
위의 [의견]을 아래 JSON 형식으로 평가하세요.
{{
    "창의적이고 혁신적인 방법인가": <15점 만점 기준 점수>,
    "단기간 내에 실현 가능한 방법인지": <10점 만점 기준 점수>,
    "총점": <총점> 
}}
"""

# 프롬프트 실행 ################################################################
def request_gpt(message, model, temperature, type="json_object"):
    message = [{"role": "user", "content": message}] 
    response = client.chat.completions.create(
                model=model,
                messages=message,
                temperature=temperature,
                response_format = {"type" : type}
            ).model_dump()
    if type == "json_object":
        response_content = json.loads(response['choices'][0]['message']['content'])
    else:
        response_content = response['choices'][0]['message']['content']
    return response_content

def generate_thoughts(selected):
    selected = "없음" if len(selected) == 0 else selected
    samples = []
    message = sampling_tempalte.format(agenda=agenda, selected=selected)
    for _ in range(5):
        sample = request_gpt(message, "gpt-4o-mini-2024-07-18", temperature=1.2)
        samples.append(sample['구현'])
        #print("generate_thoughts:", sample['구현'])
    return samples

def evaluate(thoughts):
    values = []    
    for thought in thoughts:
        message = evaluation_template.format(agenda=agenda, thought=thought)
        value = request_gpt(message, "gpt-4o-2024-05-13", temperature=0)
        values.append({
            "thought": thought,
            "value": value
        })    
    return values

def get_top_n(values, n):
    return sorted(values, key=lambda x: x["value"]["총점"], reverse=True)[:n]

selected_list = []
selected = ""
for step in range(3):
    thoughts = generate_thoughts(selected)
    values = evaluate(thoughts)
    selected = get_top_n(values, 1)[0]['thought']
    selected_list.append(selected)
    print(f"{step + 1}단계: {selected}")

print("\n".join(selected_list))


# 보고서 작성 ################################################################
summary = f"{agenda} 다음 내용을 근거로 짧은 보고서를 작성하세요:"+str(selected_list)
report = request_gpt(summary, "gpt-4o-2024-05-13", temperature=0, type="text")
print(report)
