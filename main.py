```python
import os
import requests
from datetime import datetime, timedelta

# API key
api_key = os.getenv("FOOTBALL_API_KEY")

# Server酱 key
sendkey = os.getenv("SERVERCHAN_KEY")

headers = {
    "x-apisports-key": api_key
}

# 查询昨天比赛
yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

url = f"https://v3.football.api-sports.io/fixtures?date={yesterday}"

response = requests.get(url, headers=headers)

data = response.json()

print(data)

msg = "⚽ 昨夜足球战报\n\n"

# 关注球队
favorite_teams = [
    "Manchester City",
    "Henan Songshan Longmen",
    "China",
    "China U23",
    "China U20",
    "China U17"
]

# 关注联赛
favorite_leagues = [
    "Premier League",
    "La Liga",
    "Chinese Super League"
]

if "response" in data:

    for match in data["response"]:

        status = match["fixture"]["status"]["short"]

        # 只统计已结束比赛
        if status != "FT":
            continue

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        league = match["league"]["name"]

        if (
            home in favorite_teams
            or away in favorite_teams
            or league in favorite_leagues
        ):

            fixture_id = match["fixture"]["id"]

            home_goal = match["goals"]["home"]
            away_goal = match["goals"]["away"]

            msg += (
                f"【{league}】\n"
                f"{home} {home_goal}-{away_goal} {away}\n"
            )

            # 获取比赛事件
            event_url = (
                f"https://v3.football.api-sports.io/fixtures/events?fixture={fixture_id}"
            )

            event_response = requests.get(
                event_url,
                headers=headers
            )

            event_data = event_response.json()

            if "response" in event_data:

                for event in event_data["response"]:

                    minute = event["time"]["elapsed"]

                    player = event["player"]["name"]

                    event_type = event["type"]

                    detail = event["detail"]

                    # 进球
                    if event_type == "Goal":

                        msg += (
                            f"⚽{minute}' {player}\n"
                        )

                    # 黄牌
                    elif detail == "Yellow Card":

                        msg += (
                            f"🟨{minute}' {player}\n"
                        )

                    # 红牌
                    elif detail == "Red Card":

                        msg += (
                            f"🟥{minute}' {player}\n"
                        )

            msg += "\n━━━━━━━━━━━━\n\n"

if msg == "⚽ 昨夜足球战报\n\n":
    msg += "昨天没有关注赛事的比赛。"

# Server酱推送
push_url = f"https://sctapi.ftqq.com/{sendkey}.send"

requests.post(
    push_url,
    data={
        "title": "⚽ 足球晨报",
        "desp": msg
    }
)
```
