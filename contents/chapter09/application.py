from flask import Flask, render_template, request
import sys
from common import model
from chatbot import Chatbot
from characters import system_role, instruction
#from function_calling import FunctionCalling, func_specs # 단일 함수 호출
from parallel_function_calling import FunctionCalling, tools # 병렬적 함수 호출

# jjinchin 인스턴스 생성
jjinchin = Chatbot(
    model = model.basic,
    system_role = system_role,
    instruction = instruction    
)

application = Flask(__name__)

func_calling = FunctionCalling(model=model.basic)

@application.route("/")
def hello():
    return "Hello goorm!"

@application.route("/welcome")
def welcome(): # 함수명은 꼭 welcome일 필요는 없습니다.
    return "Hello goorm!"

@application.route("/chat-app")
def chat_app():
    return render_template("chat.html")

@application.route('/chat-api', methods=['POST'])
def chat_api():        
    request_message = request.json['request_message']
    print("request_message:", request_message)
    jjinchin.add_user_message(request_message)

    # 챗GPT에게 함수사양을 토대로 사용자 메시지에 호응하는 함수 정보를 분석해달라고 요청
    #analyzed_dict = func_calling.analyze(request_message, func_specs) # 단일 함수 호출
    analyzed, analyzed_dict = func_calling.analyze(request_message, tools) # 병렬적 함수 호춝 
    # 챗GPT가 함수 호출이 필요하다고 분석했는지 여부 체크
    #if analyzed_dict.get("function_call"): # 단일 함수 호출
    if analyzed_dict.get("tool_calls"): # 병렬적 함수 호출
        # 챗GPT가 분석해준 대로 함수 호출
        #response = func_calling.run( analyzed_dict, jjinchin.context[:]) # 단일 함수 호출
        response = func_calling.run(analyzed, analyzed_dict, jjinchin.context[:]) # 병렬적 함수 호출
        jjinchin.add_response(response)
    else:
        response = jjinchin.send_request()
        jjinchin.add_response(response)

    response_message = jjinchin.get_response_content()
    jjinchin.handle_token_limit(response)
    jjinchin.clean_context()
    print("response_message:", response_message)
    return {"response_message": response_message}
 

if __name__ == "__main__":
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.jinja_env.auto_reload = True
    application.run(host="0.0.0.0", port=int(sys.argv[1]))
