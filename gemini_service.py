import requests
from config import Config

class GeminiService:
    def __init__(self):
        self.keys = Config.GEMINI_API_KEYS

    def generate(self, prompt):
        url_base = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }

        # Try each API key
        for key in self.keys:
            try:
                response = requests.post(
                    url_base + key,
                    headers=headers,
                    json=data,
                    timeout=15
                )

                if response.status_code == 429:
                    print(f"Rate limit hit for key: {key[:6]}... Trying next key.")
                    continue

                response.raise_for_status()
                result = response.json()

                return result["candidates"][0]["content"]["parts"][0]["text"]

            except requests.exceptions.RequestException as e:
                print(f"Error with key {key[:6]}: {e}")
                continue

        # If all keys fail
        return "AI system is temporarily overloaded. Please try again later."
