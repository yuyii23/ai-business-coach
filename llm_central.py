import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME") or "gpt-3.5-turbo"
API_URL = os.getenv("OPENAI_API_URL") or "https://api.openai.com/v1/chat/completions"

def ask_llm(prompt, agent=None, context=None):
    messages = []
    if context and isinstance(context, str) and context.strip():
        messages.append({"role": "system", "content": context})
    if agent:
        messages.append({"role": "system", "content": f"คุณรับบทเป็น {agent} โค้ชธุรกิจ"})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.7,
    }
    resp = requests.post(API_URL, headers=headers, json=payload)
    try:
        resp.raise_for_status()
    except Exception as e:
        print("OpenAI API response:", resp.text)
        raise e
    result = resp.json()
    return result['choices'][0]['message']['content']