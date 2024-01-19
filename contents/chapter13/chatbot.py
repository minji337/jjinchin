from common import client, makeup_response
import math
from memory_manager import MemoryManager
import threading
import time

class Chatbot:
    
    def __init__(self, model, system_role, instruction, **kwargs):
        self.context = [{"role": "system", "content": system_role}]
        self.model = model
        self.instruction = instruction
        self.max_token_size = 16 * 1024
        self.available_token_rate = 0.9
        self.user = kwargs["user"]
        self.assistant = kwargs["assistant"]
        self.memoryManager = MemoryManager(**kwargs)
        self.context.extend(self.memoryManager.restore_chat())
        # 데몬 구동
        bg_thread = threading.Thread(target=self.background_task)
        bg_thread.daemon = True
        bg_thread.start()
        
    def background_task(self):
        while True:
            self.save_chat()
            self.context = [{"role": v['role'], "content": v['content'], "saved": True} for v in self.context]
            self.memoryManager.build_memory()            
            time.sleep(3600)  # 1시간마다 반복
            #time.sleep(120)  # 테스트 용도

    def add_user_message(self, user_message):
        self.context.append({"role": "user", "content": user_message, "saved" : False})

    def _send_request(self):
        try:
            response = client.chat.completions.create(
                model=self.model, 
                messages=self.to_openai_contenxt(),
                temperature=0.5,
                top_p=1,
                max_tokens=256,
                frequency_penalty=0,
                presence_penalty=0
            ).model_dump()
        except Exception as e:
            print(f"Exception 오류({type(e)}) 발생:{e}")
            if 'maximum context length' in str(e):
                self.context.pop()
                return makeup_response("메시지 조금 짧게 보내줄래?")
            else: 
                return makeup_response("[내 찐친 챗봇에 문제가 발생했습니다. 잠시 뒤 이용해주세요]")

        return response
    
    def send_request(self):
        memory_instruction = self.retrieve_memory()
        self.context[-1]['content'] += self.instruction + (memory_instruction if memory_instruction else "")
        return self._send_request()    

    def retrieve_memory(self):
        user_message = self.context[-1]['content']
        if not self.memoryManager.needs_memory(user_message):
            return
        memory = self.memoryManager.retrieve_memory(user_message)  
        if memory is not None:
            whisper = (f"[귓속말]\n{self.assistant}야! 기억 속 대화 내용이야. 앞으로 이 내용을 참조하면서 답해줘. "
                       f"알마 전에 나누었던 대화라는 점을 자연스럽게 말해줘:\n{memory}")
            self.add_user_message(whisper)
        else:
            return "[기억이 안난다고 답할 것!]"

    def add_response(self, response):
        response_message = {
                "role" : response['choices'][0]['message']["role"],
                "content" : response['choices'][0]['message']["content"],
                "saved" : False
        }
        self.context.append(response_message)

    def get_response_content(self):
        return self.context[-1]['content']

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
    
    def to_openai_contenxt(self):
        return [{"role":v["role"], "content":v["content"]} for v in self.context]
    
    def save_chat(self):
        self.memoryManager.save_chat(self.context)            
        #pass
