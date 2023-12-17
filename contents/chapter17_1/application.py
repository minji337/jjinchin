from flask import Flask, render_template, request
import sys
from common import model, currTime
from chatbot import Chatbot
from characters import system_role, instruction
from concurrent.futures import ThreadPoolExecutor
import requests
import concurrent


#jjinchin 인스턴스 생성
jjinchin = Chatbot(
    model = model.basic,
    system_role = system_role,
    instruction = instruction    
)

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello goorm!" 

def format_response(resp, useCallback=False):
    data = {
            "version": "2.0",
            "useCallback": useCallback,
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": resp
                        }
                    }
                ]
            }
        }
    return data

executor = ThreadPoolExecutor(max_workers=1)

# 콜백 적용 전 코드
@application.route('/chat-kakao', methods=['POST'])
def chat_kakao():
    print("request.json:", request.json)
    request_message = request.json['userRequest']['utterance']
    print("request_message:", request_message)
    jjinchin.add_user_message(request_message)
    response = jjinchin.send_request()
    jjinchin.add_response(response)
    response_message = jjinchin.get_response_content()
    jjinchin.handle_token_limit(response)
    jjinchin.clean_context()    
    print("response_message:", response_message)
    return format_response(response_message)

# 비동기 호출 개선 전 코드
# def async_send_request(chat_gpt, user_message, callbackUrl):
#     chat_gpt.add_user_message(user_message)
#     response = chat_gpt.send_request()
#     chat_gpt.add_response(response)
#     response_message = chat_gpt.get_response_content()
#     print("response_message:", response_message)
#     chat_gpt.handle_token_limit(response)
#     chat_gpt.clean_context()    
#     response_to_kakao = format_response(response_message, useCallback=False)
#     callbackResponse = requests.post(callbackUrl, json=response_to_kakao)
#     print("CallbackResponse:", callbackResponse.text)
#     print(f"{'-'*50}\n{currTime()} requests.post 완료\n{'-'*50}")

# @application.route('/chat-kakao', methods=['POST'])
# def chat_kakao():
#     print(f"{'-'*50}\n{currTime()} chat-kakao 시작\n{'-'*50}")
#     print("request.json:", request.json)
#     request_message = request.json['userRequest']['utterance']
#     callbackUrl = request.json['userRequest']['callbackUrl']    
#     executor.submit(async_send_request, jjinchin, request_message, callbackUrl)
#     immediate_response = format_response("", useCallback=True)
#     print("immediate_response",immediate_response)
#     return immediate_response

    
def async_send_request(chat_gpt, callbackUrl, future):
    # future가 완료될 때까지 대기. 이후는 개선 전 코드와 동일
    response = future.result()
    chat_gpt.add_response(response)
    response_message = chat_gpt.get_response_content()
    print("response_message:", response_message)
    chat_gpt.handle_token_limit(response)
    chat_gpt.clean_context()            
    response_to_kakao = format_response(response_message, useCallback=False)
    callbackResponse = requests.post(callbackUrl, json=response_to_kakao)
    print("CallbackResponse:", callbackResponse.text)
    print(f"{'-'*50}\n{currTime()} requests.post 완료\n{'-'*50}")
    

# @application.route('/chat-kakao', methods=['POST'])
# def chat_kakao():
#     print(f"{'-'*50}\n{currTime()} chat-kakao 시작\n{'-'*50}")
#     print("request.json:", request.json)
#     request_message = request.json['userRequest']['utterance']
#     callbackUrl = request.json['userRequest']['callbackUrl']    
#     # jjinchin 객체에 사용자 메시지를 미리 넣어 둠
#     jjinchin.add_user_message(request_message)
#     # jjinchin.send_request 메소드가 실행될 미래를 담고 있는 future 객체 반환 
#     future = executor.submit(jjinchin.send_request)    
#     try:
#         # jjinchin.send_request가 종료되면 그 결과를 반환
#         # 단, 4초까지 기다리다가 완료가 안되면 concurrent.futures.TimeoutError 예외 발생 
#         response_from_openai = future.result(timeout=4)
#         jjinchin.add_response(response_from_openai)
#         response_to_kakao = format_response(jjinchin.get_response_content(), useCallback=False)
#         print("4초 내 응답:", response_to_kakao)
#         return response_to_kakao
#     except concurrent.futures.TimeoutError:
#         # 4초가 지난 경우 비동기적으로 응답결과를 보냄. 
#         # 이때 jjinchin.send_request의 미래를 담고 있는 future도 함께 넘김 
#         executor.submit(async_send_request, jjinchin, callbackUrl, future)
#         # 콜백으로 응답 예정이라는 의사표현을 함(개선 전 코드와 동일)
#         immediate_response = format_response("", useCallback=True)
#         print("콜백 응답 예정")
#         return immediate_response


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
