import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Loads values from a .env file into environment

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET_TOKEN")

def setup_webhook():
    """Configure Telegram webhook"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    payload = {
        "url": WEBHOOK_URL,
        "secret_token": WEBHOOK_SECRET,
        "allowed_updates": ["message", "callback_query", "inline_query"]
    }
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 200:
        print("✅ Webhook configured successfully!")
    else:
        print("❌ Webhook configuration failed!")

if __name__ == "__main__":
    setup_webhook()
