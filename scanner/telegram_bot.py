import os
import requests

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def send_telegram_message_with_image(message, image_path):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(image_path, "rb") as image:
        files = {"photo": image}
        data = {"chat_id": chat_id, "caption": message, "parse_mode": "HTML"}
        requests.post(url, files=files, data=data)
