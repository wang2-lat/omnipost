from platforms.reddit import RedditPlatform
from platforms.discord import DiscordPlatform
from platforms.telegram import TelegramPlatform

def get_platform(name: str, config):
    platforms = {
        "reddit": RedditPlatform,
        "discord": DiscordPlatform,
        "telegram": TelegramPlatform
    }
    
    if name not in platforms:
        raise ValueError(f"Unknown platform: {name}")
    
    return platforms[name](config)
