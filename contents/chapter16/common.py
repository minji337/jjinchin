import os
from openai import OpenAI
from dataclasses import dataclass
import pytz
from datetime import datetime, timedelta
import tiktoken


@dataclass(frozen=True)
class Model:
    basic: str = "gpt-4o-mini-2024-07-18"
    advanced: str = "gpt-4o-2024-05-13"


model = Model()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=30, max_retries=1)


def makeup_response(message, finish_reason="ERROR"):
    return {
        "choices": [
            {
                "finish_reason": finish_reason,
                "index": 0,
                "message": {"role": "assistant", "content": message},
            }
        ],
        "usage": {"total_tokens": 0},
    }


def gpt_num_tokens(messages, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    tokens_per_message = (
        3  ## 모든 메시지는 다음 형식을 따른다: <|start|>{role/name}\n{content}<|end|>\n
    )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message  #
        for _, value in message.items():
            num_tokens += len(encoding.encode(value))
    num_tokens += 3  # 모든 메시지는 다음 형식으로 assistant의 응답을 준비한다: <|start|>assistant<|message|>
    return num_tokens


def today():
    korea = pytz.timezone("Asia/Seoul")  # 한국 시간대를 얻습니다.
    now = datetime.now(korea)  # 현재 시각을 얻습니다.
    return now.strftime("%Y%m%d")  # 시각을 원하는 형식의 문자열로 변환합니다.


def yesterday():
    korea = pytz.timezone("Asia/Seoul")  # 한국 시간대를 얻습니다.
    now = datetime.now(korea)  # 현재 시각을 얻습니다.
    one_day = timedelta(days=1)  # 하루 (1일)를 나타내는 timedelta 객체를 생성합니다.
    yesterday = now - one_day  # 현재 날짜에서 하루를 빼서 어제의 날짜를 구합니다.
    return yesterday.strftime("%Y%m%d")  # 어제의 날짜를 yyyymmdd 형식으로 변환합니다.


def currTime():
    # 한국 시간대를 얻습니다.
    korea = pytz.timezone("Asia/Seoul")
    # 현재 시각을 얻습니다.
    now = datetime.now(korea)
    # 시각을 원하는 형식의 문자열로 변환합니다.
    formatted_now = now.strftime("%Y.%m.%d %H:%M:%S")
    return formatted_now
