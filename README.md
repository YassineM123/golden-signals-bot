# Golden Signals Bot

A Telegram bot built with [Telethon](https://github.com/LonamiWebs/Telethon) to forward and reformat trading signals automatically.

## 🚀 Features
- Detects and enriches trading signal messages.
- Adds branding, hashtags, and buttons.
- Copies media and messages between channels.

## ⚙️ Setup
```bash
git clone https://github.com/YOUR_USERNAME/golden-signals-bot.git
cd golden-signals-bot
pip install -r requirements.txt
cp config.example.json config.json
```
Then edit `config.json` with your own credentials from [my.telegram.org](https://my.telegram.org).

## ▶️ Run
```bash
python bot.py
```

⚠️ **Never commit your real `config.json` or `.session` files.**
