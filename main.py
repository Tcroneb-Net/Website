import os
import json
import requests
from flask import Flask, request, render_template, jsonify, send_from_directory
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

client = MongoClient(MONGO_URI)
db = client["tcroneb_bot"]
chats = db["chats"]

def generate_gemini_reply(user_input):
    prompt_context = f"""
You are an uplifting and cheerful assistant who knows:
- tcroneb, tech enthusiast and owner of Paid Tech Zone
- keketso, tba, infinity ZW: friends of tcroneb
- icon tech, owner of Queen Ruva WhatsApp bot
- Cruz, a Zimbabwean trader from Epworth with great trading experience

Always reply warmly, add friendly positivity, and make users smile. 
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_context + "\nUser: " + user_input
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "🌟 Oops! Something went wrong, but keep smiling!"

@app.route(f"/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = generate_gemini_reply(text)
        chats.insert_one({"chat_id": chat_id, "user_message": text, "bot_reply": reply})

        requests.post(
            f"{BOT_URL}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return {"ok": True}

if __name__ == "__main__":
    app.run(port=5000)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    reply = generate_gemini_reply(user_input)
    chats.insert_one({"user_message": user_input, "bot_reply": reply})
    return jsonify({"reply": reply})
