import requests
from pathlib import Path
from platforms.base import BasePlatform

class RedditPlatform(BasePlatform):
    def post(self, message: str, image: Path = None) -> dict:
        client_id = self.config.get("REDDIT_CLIENT_ID")
        client_secret = self.config.get("REDDIT_CLIENT_SECRET")
        username = self.config.get("REDDIT_USERNAME")
        password = self.config.get("REDDIT_PASSWORD")
        
        if not all([client_id, client_secret, username, password]):
            raise ValueError("Reddit credentials not configured")
        
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        data = {
            "grant_type": "password",
            "username": username,
            "password": password
        }
        headers = {"User-Agent": "omnipost/1.0"}
        
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers=headers
        )
        response.raise_for_status()
        token = response.json()["access_token"]
        
        headers["Authorization"] = f"bearer {token}"
        post_data = {
            "title": message[:300],
            "text": message,
            "sr": "u_" + username,
            "kind": "self"
        }
        
        response = requests.post(
            "https://oauth.reddit.com/api/submit",
            headers=headers,
            data=post_data
        )
        response.raise_for_status()
        
        return {"status": "posted", "response": response.json()}
