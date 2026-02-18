import requests
from config import Config

class GeminiService:
    def __init__(self):
        self.keys = Config.GEMINI_API_KEYS
        self.current_index = 0

    def get_next_key(self):
        key = self.keys[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.keys)
        return key

    def generate(self, prompt):
        api_key = self.get_next_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        response = requests.post(url, headers=headers, json=data)
        print("Gemini API Response:", response.text)  # Debugging line
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
