from pathlib import Path
from datetime import datetime
import yaml

class Storage:
    def __init__(self, storage_file: str = "posts_history.yaml"):
        self.storage_file = Path(storage_file)
        if not self.storage_file.exists():
            self.storage_file.write_text("posts: []\n")
    
    def save_post(self, message: str, results: list, image: Path = None):
        data = self._load()
        post = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message,
            "image": str(image) if image else None,
            "results": results
        }
        data["posts"].insert(0, post)
        self._save(data)
    
    def get_history(self, limit: int = 10) -> list:
        data = self._load()
        return data["posts"][:limit]
    
    def _load(self) -> dict:
        with open(self.storage_file, "r") as f:
            return yaml.safe_load(f) or {"posts": []}
    
    def _save(self, data: dict):
        with open(self.storage_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
