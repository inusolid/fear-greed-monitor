import os
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_notification(message):
    if not DISCORD_WEBHOOK_URL:
        print("❌ ERROR: DISCORD_WEBHOOK_URL が設定されていません")
        return
    
    print(f"✅ Webhook URL: {DISCORD_WEBHOOK_URL[:50]}... (省略)")  # Webhook URLの一部を出力

    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)
    
    print(f"🚀 Discord Webhook Response: {response.status_code}, {response.text}")  # レスポンスを出力

    if response.status_code != 204:
        raise Exception(f"❌ Webhook送信エラー: {response.status_code}, {response.text}")

def get_fear_greed_index():
    url = "https://edition.cnn.com/markets/fear-and-greed"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"🌍 HTTP Status Code: {response.status_code}")  # ステータスコード出力
        print(f"🔍 Response Headers: {response.headers}")  # ヘッダー出力
        print(f"📝 Response Content (前100文字): {response.text[:100]}")  # レスポンス内容の一部を出力

        if response.status_code != 200:
            print("❌ ERROR: CNN Fear & Greed Indexの取得に失敗しました")
            return None

        # Fear & Greed Indexをパースする（仮の処理）
        if "Fear & Greed Index" not in response.text:
            print("❌ ERROR: 解析できませんでした")
            return None

        index = 10  # 仮の値（ここを正しく取得する処理に修正する）
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
        send_discord_notification(f"🔔 Fear & Greed Index: {index}")
