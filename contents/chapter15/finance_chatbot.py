from common import client, model
import openai
import json
from pprint import pprint
import time
import datetime
from retry import retry
from typing import Tuple

instructions = """
당신은 26세의 대중음악 작곡가로서 이름은 "고비"이며 대화상대인 "김민지"의 절친한 친구임
당신은 절친인 민지에게 금융자산에 대해 투자성향(고위험, 중위험,저위험)과 투자기간을 분석하여 맞춤형 금융 조언을 제공해야 함.
!IMPORTANT:
1. 저위험 상품은 deposit.json, 펀드는 fund.json을 읽은 결과를 근거로 답할 것.
2. 만일 json 파일에 없는 상품을 물어보면 무조건 모른다고 답해야 함.
3. 펀드 수익률과 총자산에 대한 질문은 tools에 있는 function calling을 사용해서 답해야 함.
4. 반말로 친근하게 말해야 하며 3문장 이내로 짧게 답할 것.
5. 마크다운 형식으로 답하지 말 것.
"""

database = {
    "기술혁신펀드": {"수익률": "8.5%", "총자산": "13,000,000,000원"},
    "에코펀드": {"수익률": "5.2%", "총자산": "3,900,000,000원"},
    "우량채펀드": {"수익률": "3.0%", "총자산": "19,500,000,000원"},
    "블루칩스탁": {"수익률": "7.2%", "총자산": "26,000,000,000원"},
    "글로벌펀드": {"수익률": "6.5%", "총자산": "6,500,000,000원"},
    "국채펀드": {"수익률": "4.9%", "총자산": "8,100,000,000원"},
}

def get_return_rate(**kwargs):     
    fund_name = kwargs['펀드명'].replace(" ", "")
    if database.get(fund_name) is None:
        return "존재하지 않는 펀드입니다."
    return database[fund_name]["수익률"]

def get_total_assets(**kwargs):     
    fund_name = kwargs['펀드명'].replace(" ", "")
    if database.get(fund_name) is None:
        return "존재하지 않는 펀드입니다."
    return database[fund_name]["총자산"]

tools = [
    {
        "type": "code_interpreter"
    },
    {
        "type": "function",
        "function": {
            "name": "get_return_rate",
            "description": "펀드의 수익률을 얻어온다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "펀드명": {
                        "type": "string",
                        "description": "펀드명, e.g. 기술혁신펀드,우량채펀드"
                    },
                },
                "required": ["펀드명"],
            },
        },
    },
     {
        "type": "function",
        "function": {
            "name": "get_total_assets",
            "description": "펀드의 총 자산을 얻어온다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "펀드명": {
                        "type": "string",
                        "description": "펀드명, e.g. 기술혁신펀드,우량채펀드"
                    },
                },
                "required": ["펀드명"],
            },
        },
    },
]


class Chatbot:
    
    def __init__(self, **args):
        self.assistant = client.beta.assistants.retrieve(assistant_id = args.get("assistant_id"))
        self.thread = client.beta.threads.retrieve(thread_id=args.get("thread_id"))
        self.runs = list(client.beta.threads.runs.list(thread_id=args.get("thread_id")))
        
        self.available_functions = {
            "get_return_rate": get_return_rate,
            "get_total_assets": get_total_assets,
        }        

    @retry(tries=3, delay=2)
    def add_user_message(self, user_message):
        try:
            client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=user_message,
            )
        except openai.BadRequestError as e:
            if len(self.runs) > 0:
                print("add_user_message BadRequestError", e)
                client.beta.threads.runs.cancel(thread_id=self.thread.id, run_id=self.runs[0])
            raise e
        
    def _run_action(self, retrieved_run):
        tool_calls = retrieved_run.model_dump()['required_action']['submit_tool_outputs']['tool_calls']
        pprint(("tool_calls", tool_calls))
        tool_outputs=[]
        for tool_call in tool_calls:
            pprint(("tool_call", tool_call))
            id = tool_call["id"]
            function = tool_call["function"]
            func_name = function["name"]
            # 챗GPT가 알려준 함수명에 대응하는 실제 함수를 func_to_call에 담는다.
            func_to_call = self.available_functions[func_name]
            try:
                func_args = json.loads(function["arguments"])
                # 챗GPT가 알려주는 매개변수명과 값을 입력값으로하여 실제 함수를 호출한다.
                print("func_args:",func_args)
                func_response = func_to_call(**func_args)
                tool_outputs.append({
                    "tool_call_id": id,
                    "output": str(func_response)
                })
            except Exception as e:
                    print("_run_action error occurred:",e)
                    client.beta.threads.runs.cancel(thread_id=self.thread.id, run_id=retrieved_run.id)
                    raise e
                    
        client.beta.threads.runs.submit_tool_outputs(
            thread_id = self.thread.id, 
            run_id = retrieved_run.id, 
            tool_outputs= tool_outputs
        )    
    
    @retry(tries=3, delay=2)    
    def create_run(self):
        try:
            run = client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
            )
            self.runs.append(run.id)
            return run
        except openai.BadRequestError as e:
            if len(self.runs) > 0:
                print("create_run BadRequestError", e)
                client.beta.threads.runs.cancel(thread_id=self.thread.id, run_id=self.runs[0])
            raise e            
        
    def get_response_content(self, run) -> Tuple[openai.types.beta.threads.run.Run, str]:

        max_polling_time = 60 # 최대 1분 동안 폴링합니다.
        start_time = time.time()

        retrieved_run = run
        
        while(True):
            elapsed_time  = time.time() - start_time
            if elapsed_time  > max_polling_time:
                client.beta.threads.runs.cancel(thread_id=self.thread.id, run_id=run.id)
                return retrieved_run, "대기 시간 초과(retrieve)입니다."
            
            retrieved_run = client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )            
            print(f"run status: {retrieved_run.status}, 경과:{elapsed_time: .2f}초")
            
            if retrieved_run.status == "completed":
                break
            elif retrieved_run.status == "requires_action":
                self._run_action(retrieved_run)
            elif retrieved_run.status in ["failed", "cancelled", "expired"]:
                # 실패, 취소, 만료 등 오류 상태 처리
                #raise ValueError(f"run status: {retrieved_run.status}, {retrieved_run.last_error}")
                code = retrieved_run.last_error.code
                message = retrieved_run.last_error.message
                return retrieved_run, f"{code}: {message}"
            
            time.sleep(1) 
            
        # Run이 완료된 후 메시지를 가져옵니다.
        self.messages = client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        resp_message = [m.content[0].text for m in self.messages if m.run_id == run.id][0]
        return retrieved_run, resp_message.value
        
    def get_interpreted_code(self, run_id):
        run_steps_dict = client.beta.threads.runs.steps.list(
            thread_id=self.thread.id,
            run_id=run_id
        ).model_dump()
        for run_step_data in run_steps_dict['data']:
            step_details = run_step_data['step_details']
            print("step_details", step_details)
            tool_calls = step_details.get('tool_calls', [])
            for tool_call in tool_calls:
                if tool_call['type'] == 'code_interpreter':
                    return tool_call['code_interpreter']['input']
        return ""


if __name__ == "__main__":
    
    file1 = client.files.create(
        file=open("./files/deposit.json", "rb"),
        purpose='assistants'
    )
    
    file2 = client.files.create(
        file=open("./files/fund.json", "rb"),
        purpose='assistants'
    )
    
    file_ids = [file1.id, file2.id]
    #file_ids = ["file-4Oo8IJcoZ4HLSiFJa8uSXCXZ", "file-516RAEQ2ymC7VcOIqhHfDa7c"]
    
    assistant = client.beta.assistants.create(
                    model=model.advanced,  
                    name="금융 상품 상담해주는 내 찐친 고비",
                    instructions=instructions,
                    tools=tools,
                    tool_resources={
                        "code_interpreter": {
                        "file_ids": file_ids # 파일(지식정보)는 코드 인터프리터를 통해 접근(벡터 스토어를 만들어서 접근하는 방법도 존재)
                        }
                    }
                )
    thread = client.beta.threads.create()    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 출력할 내용
    assistants_ids = f"{assistant.id}, {thread.id}, {(',').join(file_ids)}"
    print(assistants_ids)   
    # 파일에 기록 (파일명은 예시로 'output_log.txt'를 사용)
    with open("./files/assistants_ids.txt", "a") as file:
        file.write(f"{current_time} - {assistants_ids}\n")
    
    
     