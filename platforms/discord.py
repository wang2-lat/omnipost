import requests
from pathlib import Path
from platforms.base import BasePlatform

class DiscordPlatform(BasePlatform):
    def post(self, message: str, image: Path = None) -> dict:
        webhook_url = self.config.get("DISCORD_WEBHOOK_URL")
        
        if not webhook_url:
            raise ValueError("Discord webhook URL not configured")
        
        data = {"content": message}
        files = None
        
        if image and image.exists():
            files = {"file": open(image, "rb")}
        
        response = requests.post(webhook_url, data=data, files=files)
        
        if files:
            files["file"].close()
        
        response.raise_for_status()
        
        return {"status": "posted", "webhook": webhook_url}
