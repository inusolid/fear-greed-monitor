import requests
import json
import os

# Discord WebhookのURLを環境変数から取得
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def get_fear_greed_index():
    url = "https://edition.cnn.com/markets/fear-and-greed"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    # Fear & Greed Indexの数値を抽出
    match = response.text.split('"fearGreedIndex":')
    if len(match) < 2:
        return None
    index = int(match[1].split(",")[0])

    return index

def send_discord_notification(message):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})

if __name__ == "__main__":
    index = get_fear_greed_index()
    if index is None:
        print("Error: Failed to fetch Fear & Greed Index")
    else:
        if index <= 10:
            send_discord_notification(f"🚨 Fear & Greed Index が **{index}** になりました！市場が極端な恐怖状態です。")
        elif index <= 20:
            send_discord_notification(f"⚠️ Fear & Greed Index が **{index}** になりました！恐怖が高まっています。")
