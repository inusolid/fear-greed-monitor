import os
import requests
from yahoo_fin import stock_info as si  # Yahoo Finance APIを利用

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
    """Yahoo FinanceからFear & Greed Indexを取得"""
    try:
        # Fear & Greed Indexの取得
        index = si.get_quote_table("^FNG", dict_result=True)["Previous Close"]
        index = int(index)  # 整数に変換

        print(f"✅ Fear & Greed Index: {index}")
        return index

    except Exception as e:
        print(f"❌ ERROR: Fear & Greed Indexの取得に失敗 - {str(e)}")
        return None

if __name__ == "__main__":
    index = get_fear_greed_index()
    if index is None:
        print("❌ ERROR: Failed to fetch Fear & Greed Index")
    else:
        # **ここで通知のしきい値を変更**
        if index <= 20:  # 20以下の場合に通知
            send_discord_notification(f"🔔 Fear & Greed Index: {index}")
