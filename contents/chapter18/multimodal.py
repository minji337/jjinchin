from common import model, client
import base64
import requests
import json

def ask_image(image_file, jjinchin):
    user_message = jjinchin.context[-1]['content'] + jjinchin.instruction
    prompt = f"절친이 이 이미지에 대해 다음과 같이 말하고 있습니다.:\n{user_message}"
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return ask_gpt_vision(prompt, encoded_image)

def ask_gpt_vision(prompt, encoded_image):        
    context = [{
        "role": "user",
        "content": [
            {"type": "text",
            "text": prompt},
            {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
        ]}
    ]
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=context,
        max_tokens=300,
    )    
    return response.model_dump()

def is_drawing_request(user_message):    
    message = f"다음의 JSON 타입으로 답할 것:\n {{'[{user_message}]이라는 메시지가 그림을 그려 달라는 요청인가?': <true/false>}}"
    try:
        response = client.chat.completions.create(
            model = model.basic,
            messages = [
                {"role": "user", "content": message}
            ],
            temperature = 0,
            response_format={ "type": "json_object" }
        ).model_dump()    
        print(json.loads(response['choices'][0]['message']['content']))    
        return next(iter(json.loads(response['choices'][0]['message']['content']).values()))
    except Exception as e:
        print(f"Exception 오류({type(e)}) 발생:{e}")
        return False

def create_image(jjinchin):    
    user_message = jjinchin.context[-1]['content'] + "단, 배경색은 하얀색으로 할 것"        
    url_response = client.images.generate(
        model = "dall-e-3",
        prompt = user_message,
        size="1792x1024",
        quality = "standard",
        n=1,
    )    
    
    print("url_response.data[0].url: ", url_response.data[0].url)
    
    # 이미지를 요청하고 응답을 받습니다
    image_response = requests.get(url_response.data[0].url)
    # 요청이 성공했는지 확인합니다 (200 OK)
    if image_response.status_code == 200:
        prompt = f"{user_message}=> 당신은 민지에게 다음 그림을 그려 주었습니다. 왜 이런 그림을 그렸는지 설명하세요.:\n{jjinchin.instruction}"
        encoded_image = base64.b64encode(image_response.content).decode('utf-8')        
        response = ask_gpt_vision(prompt, encoded_image)
        return encoded_image, response        
    else:
        return None, "지금은 그림을 그리기가 좀 힘드네. 다음에 그려줄게 미안해!"
    
def generate_speech(user_message):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova", #alloy, echo, fable, onyx, nova, shimmer 중 택1
            input=user_message,
        )
        return response.content
    except Exception as e:
        print(f"Exception 오류({type(e)}) 발생:{e}")
        return ""
    
    