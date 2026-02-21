from abc import ABC, abstractmethod
from pathlib import Path

class BasePlatform(ABC):
    def __init__(self, config):
        self.config = config
    
    @abstractmethod
    def post(self, message: str, image: Path = None) -> dict:
        pass
