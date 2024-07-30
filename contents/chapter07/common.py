import os
from openai import OpenAI
from dataclasses import dataclass

@dataclass(frozen=True)
class Model: 
    basic: str = "gpt-4o-mini-2024-07-18"
    advanced: str = "gpt-4o-2024-05-13"
    
model = Model();    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=30, max_retries=1)

