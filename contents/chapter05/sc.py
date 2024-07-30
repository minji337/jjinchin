import openai
import os
from collections import defaultdict
import re

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

template = """
질문1: 
공항 A에서 4대의 다른 무게의 헬리콥터를 모두 공항 B로 옮겨야 합니다. 헬리콥터의 무게는 1톤, 3톤, 6톤, 9톤이며, 이 헬리콥터가 공항 A에서 공항 B까지 이동하는 데 걸리는 시간은 각각 2시간, 3시간, 5시간, 10시간입니다. 모든 헬리콥터는 그보다 가벼운 헬리콥터를 딱 한 대만 실을 수 있습니다. 이 경우 이동하는 데 걸리는 시간은 둘 중 무거운 헬리콥터의 이동시간과 같습니다. 가장 빠르게 옮기면 몇시간이 걸릴까요?
답변:
3톤 헬리콥터에 1톤 헬리콥터를 싣고 공항 B로 이동합니다. 이동에는 3시간이 걸립니다.
3톤 헬리콥터가 공항 A로 돌아옵니다. 다시 3시간이 걸립니다. (지금까지 6시간)
9톤 헬리콥터에 6톤 헬리콥터를 싣고 공항 B로 이동합니다. 이동에는 10시간이 걸립니다. (지금까지 16시간)
공항 A에 있는 1톤 헬리콥터를 타고 공항 B로 돌아옵니다. 2시간이 걸립니다. (지금까지 18시간)
마지막으로, 3톤 헬리콥터에 1톤 헬리콥터를 싣고 공항 B로 이동합니다. 이동에는 3시간이 걸립니다. (지금까지 21시간)
정답: 21시간
```
질문2: 
닭, 쌀, 과일을 마을로 옮겨야 합니다. 닭은 1시간, 쌀은 2시간, 과일은 4시간이 소요됩니다. 농장에서 마을까지 이동하는 데는 최대 9시간이 걸릴 수 있습니다. 닭은 쌀과 과일을 먹을 수 있으므로 닭과 쌀 또는 과일을 동시에 옮길 수 없습니다. 어떻게 해야 마을로 모든 물건을 옮길 수 있을까요?
답변:
닭을 먼저 마을로 보냅니다. 이동 1시간, 총합 1시간.
농장으로 돌아옵니다. 이동 1시간, 총합 2시간.
과일을 마을로 보냅니다. 이동 4시간, 총합 6시간.
닭을 다시 농장으로 데려옵니다. 이동 1시간, 총합 7시간.
쌀을 마을로 보냅니다. 이동 2시간, 총합 9시간.
정답: 9시간
```
질문3:
4명의 탐험가가 동굴을 탐험하려고 합니다. 각 탐험가는 동굴을 지나가는 데 다음과 같은 시간이 걸립니다: 1분, 2분, 5분, 10분. 한 번에 최대 두 명만 동굴을 지날 수 있으며, 그들은 횃불을 가지고 가야 합니다. 횃불은 하나뿐이며, 탐험가가 동굴을 지나갈 때마다 횃불을 가져가야 합니다. 모든 탐험가가 동굴을 지나가려면 어떻게 해야 가장 빠르게 지나갈 수 있을까요? 마지막에 소요시간을 '정답:<정답>' 형식으로 작성하세요.
답변:
"""
def get_most_frequent_answer(template, iterations=10):
    answers = defaultdict(int)#존재하지 않는 키로 접근하면 0을 반환하도록 하는 함수
    
    for idx in range(iterations):
        context = [{"role": "user", "content": template}]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=context,
            temperature=0.3,
            #top_p=0,
            seed=12345,
        ).model_dump()
        response_content = response['choices'][0]['message']['content']
        print(f"\n{idx+1}번째 샘플:")
        print(response_content)
         # 답변에서 "정답: XX분" 형태로 시간을 추출
        match = re.search(r"정답: (\d+분)", response_content)
        if match:
            parsed_answer = match.group(1)
            answers[parsed_answer] += 1
            
    # 가장 빈도가 높은 답변을 선택
    sorted_answers = sorted(answers.items(), key=lambda x: x[1], reverse=True)
    print(f"\n빈도표: {sorted_answers}")
    most_frequent_answer = sorted_answers[0][0]
    return most_frequent_answer

most_frequent_answer = get_most_frequent_answer(template)
print("최빈값:", most_frequent_answer)