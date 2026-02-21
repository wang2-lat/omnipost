import requests
from pathlib import Path
from platforms.base import BasePlatform

class TelegramPlatform(BasePlatform):
    def post(self, message: str, image: Path = None) -> dict:
        bot_token = self.config.get("TELEGRAM_BOT_TOKEN")
        chat_id = self.config.get("TELEGRAM_CHAT_ID")
        
        if not all([bot_token, chat_id]):
            raise ValueError("Telegram credentials not configured")
        
        base_url = f"https://api.telegram.org/bot{bot_token}"
        
        if image and image.exists():
            with open(image, "rb") as f:
                files = {"photo": f}
                data = {"chat_id": chat_id, "caption": message}
                response = requests.post(f"{base_url}/sendPhoto", data=data, files=files)
        else:
            data = {"chat_id": chat_id, "text": message}
            response = requests.post(f"{base_url}/sendMessage", json=data)
        
        response.raise_for_status()
        
        return {"status": "posted", "message_id": response.json()["result"]["message_id"]}
