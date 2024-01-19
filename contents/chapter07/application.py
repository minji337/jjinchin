from flask import Flask, render_template, request 
import sys
from chatbot import Chatbot
from common import model

# jjinchin 인스턴스 생성
jjinchin = Chatbot(model.basic)

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello goorm!"

@application.route("/welcome")
def welcome(): # 함수명은 꼭 welcome일 필요는 없습니다.
    return "Hello goorm!"

@application.route("/chat-app")
def chat_app():
    return render_template("chat.html")

# 메아리 코드
# @application.route('/chat-api', methods=['POST'])
# def chat_api():
#     print("request.json:", request.json)
#     return {"response_message": "나도 " + request.json['request_message']}

@application.route('/chat-api', methods=['POST'])
def chat_api():
    request_message = request.json['request_message']
    print("request_message:", request_message)
    jjinchin.add_user_message(request_message)
    response = jjinchin.send_request()
    jjinchin.add_response(response)
    response_message = jjinchin.get_response_content()
    print("response_message:", response_message)
    return {"response_message": response_message}


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
