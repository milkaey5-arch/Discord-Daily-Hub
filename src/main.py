import os
from datetime import datetime

import requests

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

if not WEBHOOK:
    raise Exception("Brak sekretu DISCORD_WEBHOOK!")


def get_rates():
    url = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"
    data = requests.get(url, timeout=10).json()[0]["rates"]

    rates = {}
    for item in data:
        if item["code"] in ["USD", "EUR", "GBP"]:
            rates[item["code"]] = item["mid"]

    return rates


def get_crypto():
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum&vs_currencies=pln"
    )

    data = requests.get(url, timeout=10).json()

    return {
        "BTC": data["bitcoin"]["pln"],
        "ETH": data["ethereum"]["pln"],
    }


def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=51.3688"
        "&longitude=19.3567"
        "&current=temperature_2m"
    )

    data = requests.get(url, timeout=10).json()

    return data["current"]["temperature_2m"]


try:

    rates = get_rates()
    crypto = get_crypto()
    temp = get_weather()

    embed = {
        "title": "🌅 Daily Report",
        "description": "Automatyczny raport dnia",
        "color": 0x2ECC71,
        "fields": [
            {
                "name": "💰 Waluty",
                "value": (
                    f"🇺🇸 USD: **{rates['USD']:.2f} PLN**\n"
                    f"🇪🇺 EUR: **{rates['EUR']:.2f} PLN**\n"
                    f"🇬🇧 GBP: **{rates['GBP']:.2f} PLN**"
                ),
                "inline": False,
            },
            {
                "name": "₿ Kryptowaluty",
                "value": (
                    f"₿ BTC: **{crypto['BTC']:,.0f} PLN**\n"
                    f"Ξ ETH: **{crypto['ETH']:,.0f} PLN**"
                ),
                "inline": False,
            },
            {
                "name": "🌤 Pogoda",
                "value": (
                    f"📍 Bełchatów\n"
                    f"🌡 {temp:.1f}°C"
                ),
                "inline": False,
            },
        ],
        "footer": {
            "text": f"Wygenerowano: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        },
    }

except Exception as e:

    embed = {
        "title": "❌ Daily Report",
        "description": f"Wystąpił błąd:\n```{e}```",
        "color": 0xE74C3C,
    }


response = requests.post(
    WEBHOOK,
    json={
        "embeds": [embed]
    },
    timeout=10,
)

print(response.status_code)
print(response.text)