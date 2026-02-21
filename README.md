# OmniPost

Multi-platform social media posting CLI for niche platforms.

## Features

- Unified API credential management for Reddit, Discord, Telegram
- One-click posting to multiple platforms (text + images)
- Post history tracking and status monitoring

## Installation


## Setup

1. Create configuration file:

2. Edit `.env` file with your API credentials

## Usage

### Post to all platforms

### Post to specific platforms

### Post with image

### View posting history

### View limited history

## Platform Setup

### Reddit
1. Create app at https://www.reddit.com/prefs/apps
2. Get client ID and secret
3. Add credentials to `.env`

### Discord
1. Create webhook in Discord server settings
2. Copy webhook URL
3. Add to `.env`

### Telegram
1. Create bot via @BotFather
2. Get bot token
3. Get chat ID (send message to bot, then check https://api.telegram.org/bot<TOKEN>/getUpdates)
4. Add credentials to `.env`

## License

MIT
pip install -r requirements.txt
python main.py setup  # 生成 .env 配置文件
# 编辑 .env 填入各平台 API 凭证
python main.py post "Hello World"