import os
import requests
from datetime import datetime

# API-FOOTBALL key
api_key = os.getenv("FOOTBALL_API_KEY")

# Server酱 key
sendkey = os.getenv("SERVERCHAN_KEY")

# 查询今日比赛
today = datetime.utcnow().strftime("%Y-%m-%d")

url = f"https://v3.football.api-sports.io/fixtures?date={today}"

headers = {
    "x-apisports-key": api_key
}

headers = {
    "x-apisports-key": api_key
}

response = requests.get(url, headers=headers)

data = response.json()

print(data)

msg = ""

if "response" in data:
    for match in data["response"]:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        date = match["fixture"]["date"][:16]

        msg += f"{home} vs {away}\n{date}\n\n"

# 推送到微信
push_url = f"https://sctapi.ftqq.com/{sendkey}.send"

requests.post(
    push_url,
    data={
        "title": "⚽ 今日足球比赛",
        "desp": msg
    }
)
