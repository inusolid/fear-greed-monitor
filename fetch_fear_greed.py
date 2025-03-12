import os
import requests

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
    """Alternative.meのFear & Greed Index APIからデータを取得"""
    url = "https://api.alternative.me/fng/"
    
    try:
        response = requests.get(url)
        print(f"🌍 HTTP Status Code: {response.status_code}")  # ステータスコード出力
        print(f"📝 Response JSON: {response.json()}")  # レスポンス内容を出力

        if response.status_code != 200:
            print("❌ ERROR: Fear & Greed Indexの取得に失敗しました")
            return None

        data = response.json()
        index = int(data["data"][0]["value"])  # Fear & Greed Indexの数値を取得

        return index

    except Exception as e:
        print(f"❌ ERROR: リクエスト中に例外発生 - {str(e)}")
        return None

if __name__ == "__main__":
    index = get_fear_greed_index()
    if index is None:
        print("❌ ERROR: Failed to fetch Fear & Greed Index")
    else:
        print(f"✅ Fear & Greed Index: {index}")

        # **ここで通知のしきい値を変更**
        if index <= 20:  # 20以下の場合に通知
            send_discord_notification(f"🔔 Fear & Greed Index: {index}")
