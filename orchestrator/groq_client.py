import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_task_plan(user_request: str) -> list:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in environment.")

    # Load prompt template and insert user request
    try:
        with open("orchestrator/tasks_plan_prompt.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print("[ERROR] Prompt template not found!")
        return ["clean_text"]

    prompt = prompt_template.replace("{user_request}", user_request)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 100
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body
    )

    # Debug response
    print("[DEBUG] Groq status:", response.status_code)
    print("[DEBUG] Groq response:", response.text)

    try:
        result_text = response.json()["choices"][0]["message"]["content"]
        return json.loads(result_text)
    except Exception as e:
        print("[ERROR] Failed to parse Groq response:", str(e))
        return ["clean_text"]
