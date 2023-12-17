from common import client, model
from pprint import pprint

class Chatbot:

    def __init__(self, model):
        self.context = [{"role": "system", "content": "You are a helpful assistant."}]
        self.model = model

    def add_user_message(self, message):
        self.context.append({"role": "user", "content": message})

    def send_request(self):
        response = client.chat.completions.create(
            model=self.model, 
            messages=self.context
        ).model_dump()
        return response

    def add_response(self, response):
        self.context.append({
                "role" : response['choices'][0]['message']["role"],
                "content" : response['choices'][0]['message']["content"],
            }
        )

    def get_response_content(self):
        return self.context[-1]['content']


if __name__ == "__main__":
    # step-3: 테스트 시나리오에 따라 실행 코드 작성 및 예상 출력결과 작성
    chatbot = Chatbot(model.basic)

    chatbot.add_user_message("Who won the world series in 2020?")

    # 시나리오1-4: 현재 context를 openai api 입력값으로 설정하여 전송
    response = chatbot.send_request()

    # 시나리오1-5: 응답 메시지를 context에 추가
    chatbot.add_response(response)

    # 시나리오1-7: 응답 메시지 출력
    print(chatbot.get_response_content())

    # 시나리오2-2: 사용자가 채팅창에 "Where was it played?" 입력
    chatbot.add_user_message("Where was it played?")

    # 다시 요청 보내기
    response = chatbot.send_request()

    # 응답 메시지를 context에 추가
    chatbot.add_response(response)

    # 응답 메시지 출력
    print(chatbot.get_response_content())

    pprint(chatbot.context) 


