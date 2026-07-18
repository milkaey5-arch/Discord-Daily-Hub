import os
import requests

webhook = os.getenv("DISCORD_WEBHOOK")

if not webhook:
    raise Exception("Brak sekretu DISCORD_WEBHOOK!")

embed = {
    "title": "🚀 Discord Daily Hub",
    "description": "Pierwszy test zakończony sukcesem!",
    "color": 5763719,
    "footer": {
        "text": "Powered by GitHub Actions"
    }
}

response = requests.post(
    webhook,
    json={
        "embeds": [embed]
    }
)

print(response.status_code)
print(response.text)