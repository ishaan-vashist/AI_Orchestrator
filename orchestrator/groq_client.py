import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_task_plan(user_request: str) -> list:
    """
    Sends the user instruction to the Groq LLM and retrieves a list of tasks 
    to be executed in sequence (e.g., ['clean_text', 'summarization']).
    """
    
    # Fetch API key from environment
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in environment.")

    # Load the task planning prompt template
    try:
        with open("orchestrator/tasks_plan_prompt.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print("[ERROR] Prompt template not found!")
        return ["clean_text"]  # Fallback if prompt is missing

    # Replace placeholder with actual user request
    prompt = prompt_template.replace("{user_request}", user_request)

    # Prepare headers for the Groq API request
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Construct the chat body for the Groq model
    body = {
        "model": "llama3-8b-8192",  # You can switch models if needed
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,           # Deterministic output
        "max_tokens": 100           # Limited response length
    }

    # Make the API request to Groq
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body
    )

    # Debug log: Groq API response
    print("[DEBUG] Groq status:", response.status_code)
    print("[DEBUG] Groq response:", response.text)

    # Attempt to parse the response and return task list
    try:
        result_text = response.json()["choices"][0]["message"]["content"]
        return json.loads(result_text)  # Convert JSON string to list
    except Exception as e:
        print("[ERROR] Failed to parse Groq response:", str(e))
        return ["clean_text"]  # Fallback task if parsing fails
