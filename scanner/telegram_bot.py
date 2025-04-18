import os
import requests

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Missing Telegram credentials")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def send_chart_image(image_path, caption="📈 Chart"):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Missing Telegram credentials")
        return

    with open(image_path, "rb") as image_file:
        files = {"photo": image_file}
        data = {"chat_id": chat_id, "caption": caption}
        requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data=data, files=files)
