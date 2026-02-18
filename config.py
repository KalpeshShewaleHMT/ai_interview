import os

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Multiple Gemini API Keys
    GEMINI_API_KEYS = [
        "YOUR_GEMINI_KEY_1",
        "YOUR_GEMINI_KEY_2"
    ]
