import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def get_exchange_rate(base_currency, target_currency, api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['result'] == 'success':
            rate = data['conversion_rates'].get(target_currency)
            if rate:
                return f"{base_currency} → {target_currency}: 1 {base_currency} = {rate} {target_currency}"
            else:
                return f"找不到 {target_currency} 的匯率"
        else:
            return "查詢失敗"
    except Exception as e:
        return f"錯誤: {e}"

def get_btc_to_twd():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {'ids': 'bitcoin', 'vs_currencies': 'twd'}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        btc_rate = data['bitcoin']['twd']
        return f"BTC → TWD: 1 BTC = {btc_rate} TWD"
    except Exception as e:
        return f"查詢 BTC 錯誤: {e}"

def get_gold_and_silver_price():
    url = "https://data-asg.goldprice.org/dbXRates/USD"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        item = data['items'][0]
        gold_price = item['xauPrice']
        silver_price = item['xagPrice']
        return f"金價（XAU）: {gold_price} USD\n銀價（XAG）: {silver_price} USD"
    except Exception as e:
        return f"查詢金銀價錯誤: {e}"

def get_rates_summary():
    api_key = "1f7537b2002b5281285975b0"
    currency_list = ['USD', 'JPY', 'AUD']
    target_currency = 'TWD'

    lines = ["【法幣匯率】"]
    for currency in currency_list:
        lines.append(get_exchange_rate(currency, target_currency, api_key))

    lines.append("\n【加密貨幣匯率】")
    lines.append(get_btc_to_twd())

    lines.append("\n【貴金屬價格（美元）】")
    lines.append(get_gold_and_silver_price())

    return "\n".join(lines)

def send_email(subject, body, sender_email, receiver_email, app_password):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("✅ 郵件已寄出")
    except Exception as e:
        print("❌ 發送郵件失敗:", e)

if __name__ == "__main__":
    summary = get_rates_summary()

    sender = os.environ.get("GMAIL_USER")
    receiver = os.environ.get("RECIPIENT_EMAIL")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not receiver or not app_password:
        print("❌ 缺少寄信環境變數，請確認 GitHub Secrets 設定正確")
    else:
        send_email("每日匯率 + 金銀價格 更新", summary, sender, receiver, app_password)
