import os
import requests
from datetime import datetime

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

if not WEBHOOK:
    raise Exception("Brak sekretu DISCORD_WEBHOOK!")

# ==========================
# Kursy walut NBP
# ==========================

nbp = requests.get(
    "https://api.nbp.pl/api/exchangerates/tables/A?format=json",
    timeout=10
).json()[0]["rates"]

rates = {x["code"]: x["mid"] for x in nbp}

# ==========================
# Kryptowaluty
# ==========================

crypto = requests.get(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=pln",
    timeout=10
).json()

btc = crypto["bitcoin"]["pln"]
eth = crypto["ethereum"]["pln"]

# ==========================
# Pogoda
# ==========================

weather = requests.get(
    "https://api.open-meteo.com/v1/forecast?latitude=51.3688&longitude=19.3567&current=temperature_2m",
    timeout=10
).json()

temp = weather["current"]["temperature_2m"]

# ==========================
# Embed
# ==========================

embed = {
    "title": "🔥 NOWA WERSJA DZIAŁA 🔥",
    "description": "Jeżeli widzisz tę wiadomość, działa nowy kod z GitHub Actions.",
    "color": 3066993,
    "fields": [
        {
            "name": "💰 Waluty",
            "value": (
                f"🇺🇸 USD: {rates['USD']:.2f} PLN\n"
                f"🇪🇺 EUR: {rates['EUR']:.2f} PLN\n"
                f"🇬🇧 GBP: {rates['GBP']:.2f} PLN"
            ),
            "inline": False
        },
        {
            "name": "₿ Kryptowaluty",
            "value": (
                f"BTC: {btc:,.0f} PLN\n"
                f"ETH: {eth:,.0f} PLN"
            ),
            "inline": False
        },
        {
            "name": "🌤 Pogoda",
            "value": f"Bełchatów\n{temp}°C",
            "inline": False
        }
    ],
    "footer": {
        "text": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
}

response = requests.post(
    WEBHOOK,
    json={
        "embeds": [embed]
    },
    timeout=10
)

print(response.status_code)
print(response.text)