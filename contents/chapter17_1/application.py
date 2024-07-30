from flask import Flask, render_template, request, Response, url_for
import sys
from common import model
from chatbot import Chatbot
from characters import system_role, instruction
import multimodal

# jjinchin 인스턴스 생성
jjinchin = Chatbot(
    model = model.basic,
    system_role = system_role,
    instruction = instruction    
)

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

@application.route('/audio')
def audio_route():
    user_message = request.args.get('message', '')
    # TTS 요청
    speech = multimodal.generate_speech(user_message)
    return Response(speech, mimetype='audio/mpeg')    

@application.route('/chat-api', methods=['POST'])
def chat_api():       
    request_message = request.form.get("message")
    print("request_message:", request_message)
    jjinchin.add_user_message(request_message)
    
    response_image = None
    image_file = request.files.get('image')
    if image_file is not None:
        response = multimodal.ask_image(image_file, jjinchin)        
    elif multimodal.is_drawing_request(request_message):    
        encoded_image, response = multimodal.create_image(jjinchin)
        if encoded_image:
            response_image = f"data:image/png;base64,{encoded_image}"                    
    else:
        response = jjinchin.send_request()        
            
    jjinchin.add_response(response)        
    response_message = jjinchin.get_response_content()        
    
    jjinchin.handle_token_limit(response)
    jjinchin.clean_context()            
    
    response_audio = None    
    if response_image is not None:    
        response_audio = url_for('audio_route', message=response_message, _external=True)    
        response_message = ""
    
    print("response_message:", response_message)
    return {"response_message": response_message, "image": response_image, "audio": response_audio} 
 

if __name__ == "__main__":  
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    application.jinja_env.auto_reload = True
    application.run(host="0.0.0.0", port=int(sys.argv[1]))
esponse(response_message_from_openai, useCallback=False)
        print("3초 내 응답:", response_to_kakao)
        return response_to_kakao
    except concurrent.futures.TimeoutError:
        # 3초가 지난 경우 비동기적으로 응답결과를 보냄. 
        # 이때 jjinchin.send_request의 미래를 담고 있는 future도 함께 넘김 
        executor.submit(async_send_request, jjinchin, callbackUrl, future)
        # 콜백으로 응답 예정이라는 의사표현을 함(개선 전 코드와 동일)
        immediate_response = format_response("", useCallback=True)
        print("콜백 응답 예정")
        return immediate_response


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
tent()
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
