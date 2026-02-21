from pathlib import Path
from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
    
    def get(self, key: str, default: str = "") -> str:
        return os.getenv(key, default)
    
    def get_enabled_platforms(self) -> list:
        platforms = []
        if self.get("REDDIT_CLIENT_ID"):
            platforms.append("reddit")
        if self.get("DISCORD_WEBHOOK_URL"):
            platforms.append("discord")
        if self.get("TELEGRAM_BOT_TOKEN"):
            platforms.append("telegram")
        return platforms
