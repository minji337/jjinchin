from common import client
import math
import time
from retry import retry
import openai

class Chatbot:
    
    def __init__(self, **args):
        if args.get("assistant_id") is not None:
            self.assistant = client.beta.assistants.retrieve(assistant_id = args.get("assistant_id"))
        else:
            self.assistant = client.beta.assistants.create(
                            name=args.get("assistant_name"),
                            instructions=args.get("instructions"), 
                            model=args.get("model"),
                        )
        if args.get("thread_id") is not None:
            self.thread = client.beta.threads.retrieve(thread_id=args.get("thread_id"))
            self.runs = list(client.beta.threads.runs.list(thread_id=args.get("thread_id")))
        else:
            self.thread = client.beta.threads.create()
            self.runs = []
        
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

    def get_response_content(self, run) -> (openai.types.beta.threads.run.Run, str):
        max_polling_time = 60 # 최대 1분 동안 폴링합니다.
        start_time = time.time()
        retrieved_run = run
        while(True):
            elapsed_time  = time.time() - start_time
            if elapsed_time  > max_polling_time:
                return retrieved_run, "대기 시간 초과(retrieve)입니다."
            
            retrieved_run = client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )            
            print(f"run status: {retrieved_run.status}, 경과:{elapsed_time: .2f}초")
            
            if retrieved_run.status == "completed":
                break
            elif retrieved_run.status == "requires_action":
                pass
            elif retrieved_run.status in ["failed", "cancelled", "expired"]:
                # 실패, 취소, 만료 등 오류 상태 처리
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


    def clean_context(self):
        for idx in reversed(range(len(self.context))):
            if self.context[idx]["role"] == "user":
                self.context[idx]["content"] = self.context[idx]["content"].split("instruction:\n")[0].strip()
                break
    
    def handle_token_limit(self, response):
        # 누적 토큰 수가 임계점을 넘지 않도록 제어한다.
        try:
            current_usage_rate = response['usage']['total_tokens'] / self.max_token_size
            exceeded_token_rate = current_usage_rate - self.available_token_rate
            if exceeded_token_rate > 0:
                remove_size = math.ceil(len(self.context) / 10)
                self.context = [self.context[0]] + self.context[remove_size+1:]
        except Exception as e:
            print(f"handle_token_limit exception:{e}")

