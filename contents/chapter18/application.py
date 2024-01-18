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
    
    image_file = request.files.get('image')
    if image_file is not None:
        response = multimodal.ask_image(image_file, jjinchin)
    else:
        response = jjinchin.send_request()        
            
    response_image = None
    if multimodal.is_drawing_request(request_message):    
        encoded_image, response = multimodal.create_image(jjinchin)
        if encoded_image:
            response_image = f"data:image/png;base64,{encoded_image}"                    
        
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
