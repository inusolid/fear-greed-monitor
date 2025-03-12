import os
import requests
import re

# Discord WebhookのURLを環境変数から取得
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_notification(message):
    """Discordに通知を送信"""
    if not DISCORD_WEBHOOK_URL:
        print("❌ ERROR: DISCORD_WEBHOOK_URL が設定されていません")
        return

    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)
    
    print(f"🚀 Discord Webhook Response: {response.status_code}, {response.text}")  # レスポンスを出力

    if response.status_code != 204:
        raise Exception(f"❌ Webhook送信エラー: {response.status_code}, {response.text}")

def get_fear_greed_index():
    """CNNのFear & Greed Indexを取得"""
    url = "https://edition.cnn.com/markets/fear-and-greed"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        print(f"🌍 HTTP Status Code: {response.status_code}")  # ステータスコード出力

        if response.status_code != 200:
            print("❌ ERROR: CNN Fear & Greed Indexの取得に失敗しました")
            return None

        # Fear & Greed IndexをHTMLから取得する
        match = re.search(r'Fear & Greed Index is (\d+)', response.text)
        if not match:
            print("❌ ERROR: Fear & Greed Indexの値を取得できませんでした")
            return None

        index = int(match.group(1))
        print(f"✅ Fear & Greed Index: {index}")
        return index

    except Exception as e:
        print(f"❌ ERROR: リクエスト中に例外発生 - {str(e)}")
        return None

if __name__ == "__main__":
    index = get_fear_greed_index()
    if index is None:
        print("❌ ERROR: Failed to fetch Fear & Greed Index")
    else:
        # **ここで通知のしきい値を変更**
        if index <= 20:  # 20以下の場合に通知
            send_discord_notification(f"🔔 Fear & Greed Index: {index}")
