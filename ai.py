import requests
import json

COHERE_API_KEY = "bf5Qur8XrFgfmiAoU0KL111qbVud0P2KGQFZvdW8"

def extract_data(text):
    prompt = f"""
Extract transaction info as JSON.
Text: {text}

Return format:
{{
  "item": "",
  "customer": "",
  "total": 0,
  "paid": 0,
  "debt": 0
}}
"""

    res = requests.post(
        "https://api.cohere.com/v1/chat",
        headers={
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "command-a-03-2025",
            "message": prompt
        }
    )

    return json.loads(res.json()["text"])
