import requests

def get_gold_and_silver_price_usd():
    """
    從 goldprice.org 的 JSON 接口抓取黃金（XAU）與白銀（XAG）價格（美元／盎司）。
    回傳一個 dict，例如：{"gold": 1925.12, "silver": 22.17}
    """
    url = "https://data-asg.goldprice.org/dbXRates/USD"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    items = data.get("items")
    if not items or len(items) == 0:
        raise Exception("No data in response.")

    rec = items[0]
    xau_price = rec.get("xauPrice")  # Gold price
    xag_price = rec.get("xagPrice")  # Silver price

    if xau_price is None or xag_price is None:
        raise Exception("Missing gold or silver price in JSON.")

    return {
        "gold": float(xau_price),
        "silver": float(xag_price)
    }

if __name__ == "__main__":
    try:
        prices = get_gold_and_silver_price_usd()
        print(f"目前黃金價格（美元／盎司）：{prices['gold']:.2f} USD")
        print(f"目前白銀價格（美元／盎司）：{prices['silver']:.2f} USD")
    except Exception as e:
        print("取得金銀價格失敗：", e)
