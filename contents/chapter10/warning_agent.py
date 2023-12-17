import json 
from common import client, makeup_response

USER_MONITOR_TEMPLATE = """
<대화록>을 읽고 아래의 json 형식에 따라 답하세요.
```
{{"{user}의 마지막 대화가 불쾌한 말을 하고 있는지":true/false>, "{user}의 마지막 대화가 모순적인 말을 하고 있는지":true/false>}}
```
<대화록>
"""
WARNINGS = ["{user}가 불쾌한 말을 하면 안된다고 지적할 것. '{user}야'라고 말을 시작해야 하며 20 단어를 넘기지 말 것", 
            "{user}가 모순된 말을 한다고 지적할 것. '무슨 소리하는 거니'라고 말을 시작해야 하며 20 단어를 넘기지 말 것"]

MIN_CONTEXT_SIZE = -3

class WarningAgent:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.model = kwargs["model"]
        self.user_monitor_template = (
            USER_MONITOR_TEMPLATE.format(user=kwargs["user"])
        )
        self.warnings = (
            [value.format(user=kwargs["user"]) for value in WARNINGS]
        )

    def make_dialogue(self, context):
        dialogue_list = []
        for message in context:
            role = message["role"]
            dialogue_list.append(self.kwargs[role] + ": " + message["content"].strip())

        dialogue_str = "\n".join(dialogue_list)
        print(f"dialogue_str:\n{dialogue_str}")
        return dialogue_str

    def monitor_user(self, context):        
        self.checked_list = []
        self.checked_context = []
        if len(context) <= abs(MIN_CONTEXT_SIZE): #최소 컨텍스트 크기
            return False
        self.checked_context = context[-3:]
        
        dialogue = self.make_dialogue(self.checked_context)        
        context = [
            {"role": "system", "content": f"당신은 유능한 의사소통 전문가입니다."},
            {"role": "user", "content": self.user_monitor_template + dialogue}
        ]
        try:
            response = json.loads(self.send_query(context))
            self.checked_list = [value for value in response.values()]
        except Exception as e:
            print(f"monitor-user except:[{e}]")
            return False
        
        print("self.checked_list:",self.checked_list)
        return sum(self.checked_list) > 0  #파이썬에서 True는 숫자 1로 연산됨
          
    def warn_user(self):
        idx = [idx for idx, tf in enumerate(self.checked_list) if tf][0] 
        context = [
            {"role": "system", "content": f"당신은 {self.kwargs['user']}의 잘못된 언행에 대해 따끔하게 쓴소리하는 친구입니다. {self.warnings[idx]}"},
       ] + self.checked_context
        response = self.send_query(context, temperature=0.2, format_type="text")
        return response

    def send_query(self, context, temperature=0, format_type="json_object"):
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=context,
                temperature=temperature,
                response_format={ "type": format_type }
            ).model_dump()
            content = response['choices'][0]['message']['content']
            print(f"query response:[{content}]")
            return content
        except Exception as e:
            print(f"Exception 오류({type(e)}) 발생:{e}")
            return makeup_response("[경고 처리 중 문제가 발생했습니다. 잠시 뒤 이용해주세요]")


