from flask import Flask, render_template, request 
import sys
from finance_chatbot import Chatbot


# jjinchin 인스턴스 생성
jjinchin = Chatbot(
    assistant_id="asst_70yCniednJ6o3KWLIZAUzEE6",
    thread_id="thread_zlhXipoohwPiLXyRE42PEYP2"
)

application = Flask(__name__)

@application.route("/chat-app")
def chat_app():
    return render_template("chat.html")

@application.route('/chat-api', methods=['POST'])
def chat_api():
    request_message = request.form.get("message")     
    print("request_message:", request_message)
    try: 
        jjinchin.add_user_message(request_message)
        run = jjinchin.create_run()
        _, response_message = jjinchin.get_response_content(run)
        response_python_code = jjinchin.get_interpreted_code(run.id)
    except Exception as e:
        print("assistants ai error", e)
        response_message = "[Assistants API 오류가 발생했습니다]"
            
    print("response_message:", response_message)
    return {"response_message": response_message, "response_python_code": response_python_code}

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
