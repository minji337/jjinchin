import openai
import sys
import os
import json
from function_calling import FunctionCalling, tools_report
from common import client, model

func_calling = FunctionCalling(model=model.advanced)

template = """
[{과제}]룰 해결하기 위해 해야 할 일을 2단계로 아래 JSON 포맷으로 말하세요. 사용할 수 있는 도구에는 "인터넷검색"과 "보고서작성"이 있습니다.
```
JSON 포맷: 
{{"step-1": <1단계 할일>, "step-2": <2단계 할일>}}
"""

def create_step_plan(message):
    completion = client.chat.completions.create(
                    model=model.advanced,
                    messages=[{"role": "user", "content": message}],
                    response_format={"type": "json_object"}
                )
    return json.loads(completion.choices[0].message.content)

print('sys.argv[1]', sys.argv[1])
steps = create_step_plan(template.format(과제=sys.argv[1]))

response_message = ""
for step in steps.values():
    print("step:", step)
    user_message = f"{step}:\n{response_message}"
    _, analyzed_dict = func_calling.analyze(user_message, tools_report) 
    if analyzed_dict.get("tool_calls"):
        response_message = func_calling.call_function(analyzed_dict)

print(f"최종결과:\n{response_message}")