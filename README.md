# Tcroneb AI Telegram Bot

A Telegram bot powered by Gemini AI to chat about:
- tcroneb and Paid Tech Zone
- Friends: keketso, tba, infinity ZW
- icon tech (Queen Ruva bot owner)
- Cruz (Epworth trader)

### Setup

1. Create a `.env` file with:
```
TELEGRAM_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_api_key
MONGO_URI=your_mongodb_uri
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the bot:
```
python main.py
```

4. Set webhook for Telegram:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<your_domain>/webhook
```