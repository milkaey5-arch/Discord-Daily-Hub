import os
import requests
from datetime import datetime

webhook = os.getenv("DISCORD_WEBHOOK")

if not webhook:
    raise Exception("Brak sekretu DISCORD_WEBHOOK!")

# Kursy NBP
nbp = requests.get("https://api.nbp.pl/api/exchangerates/tables/A?format=json").json()[0]["rates"]

kursy = {}

for waluta in ["USD", "EUR", "GBP"]:
    kurs = next(x for x in nbp if x["code"] == waluta)
    kursy[waluta] = kurs["mid"]

# BTC i ETH (CoinGecko)
crypto = requests.get(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=pln"
).json()

btc = crypto["bitcoin"]["pln"]
eth = crypto["ethereum"]["pln"]

# Pogoda (Bełchatów)
weather = requests.get(
    "https://api.open-meteo.com/v1/forecast?latitude=51.3688&longitude=19.3567&current=temperature_2m"
).json()

temp = weather["current"]["temperature_2m"]

embed = {
    "title": "🌅 Daily Report",
    "color": 0x2ECC71,
    "fields": [
        {
            "name": "💰 Waluty",
            "value":
                f"🇺🇸 USD: **{kursy['USD']:.2f} PLN**\n"
                f"🇪🇺 EUR: **{kursy['EUR']:.2f} PLN**\n"
                f"🇬🇧 GBP: **{kursy['GBP']:.2f} PLN**",
            "inline": False
        },
        {
            "name": "₿ Kryptowaluty",
            "value":
                f"BTC: **{btc:,.0f} PLN**\n"
                f"ETH: **{eth:,.0f} PLN**",
            "inline": False
        },
        {
            "name": "🌤 Pogoda",
            "value": f"Bełchatów\n🌡 {temp}°C",
            "inline": False
        }
    ],
    "footer": {
        "text": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
}

requests.post(
    webhook,
    json={
        "embeds": [embed]
    }
)