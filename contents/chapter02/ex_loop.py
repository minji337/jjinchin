emotions = ['사랑', '증오', '사랑', '기쁨', '증오', '기쁨', '행복', '슬픔', '분노', '사랑']
pos_emotion_count = 0
neg_emotion_count = 0

for emotion in emotions:
    if emotion == '사랑' or emotion == '기쁨' or emotion == '행복':
    #if emotion in ['사랑', '기쁨', '행복']: 이렇게 코딩해도 동일한 결과를 얻습니다.
        pos_emotion_count = pos_emotion_count + 1 #pos_emotion_count가 1씩 누계됨
    else:
        neg_emotion_count = neg_emotion_count + 1 #neg_emotion_count가 1씩 누계됨

#len은 콜렉션 데이터의 요소들의 갯수를 알려주는 파이썬 함수입니다.
pos_emotion_rate = pos_emotion_count / len(emotions) 
neg_emotion_rate = neg_emotion_count / len(emotions)

if pos_emotion_rate >= 0.5:
    print("긍정의 감정이", pos_emotion_rate, "이므로 기분 좋습니다.")
else:
    print("부정의 감정이", neg_emotion_rate, "이므로 기분 나쁩니다.")
