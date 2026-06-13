import requests

url = "https://api.sofascore.com/api/v1/sport/football/events/live"

headers = {
"User-Agent": "Mozilla/5.0"
}

response = requests.get(
url,
headers=headers
)

print(response.status_code)

print(response.text[:500])
