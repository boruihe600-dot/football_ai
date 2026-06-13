```python
import os
import requests
from datetime import datetime, timedelta
from config import TEAM_IDS, LEAGUES, WORLD_CUP

api_key = os.getenv("FOOTBALL_API_KEY")
sendkey = os.getenv("SERVERCHAN_KEY")

headers = {
    "x-apisports-key": api_key
}

msg = "⚽ 足球日报\n\n"

# ==================
# 昨日重点比赛
# ==================
yesterday = (
    datetime.utcnow() - timedelta(days=1)
).strftime("%Y-%m-%d")

msg += "【昨日重点比赛】\n\n"

for team_name, team_id in TEAM_IDS.items():

    url = (
        f"https://v3.football.api-sports.io/fixtures"
        f"?team={team_id}&date={yesterday}"
    )

    data = requests.get(
        url,
        headers=headers
    ).json()

    if len(data["response"]) == 0:
        continue

    for match in data["response"]:

        status = match["fixture"]["status"]["short"]

        if status != "FT":
            continue

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        home_goal = match["goals"]["home"]
        away_goal = match["goals"]["away"]

        msg += (
            f"{home} {home_goal}-{away_goal} {away}\n"
        )

        fixture_id = match["fixture"]["id"]

        event_url = (
            f"https://v3.football.api-sports.io/fixtures/events"
            f"?fixture={fixture_id}"
        )

        event_data = requests.get(
            event_url,
            headers=headers
        ).json()

        for e in event_data["response"]:

            player = e["player"]["name"]
            minute = e["time"]["elapsed"]

            if e["type"] == "Goal":

                msg += (
                    f"⚽ {minute}' {player}\n"
                )

            elif e["detail"] == "Yellow Card":

                msg += (
                    f"🟨 {minute}' {player}\n"
                )

            elif e["detail"] == "Red Card":

                msg += (
                    f"🟥 {minute}' {player}\n"
                )

        msg += "\n"

# ==================
# 积分榜
# ==================

season = datetime.now().year

for league_name, league_id in LEAGUES.items():

    msg += (
        f"\n【{league_name}积分榜】\n"
    )

    url = (
        "https://v3.football.api-sports.io/standings"
        f"?league={league_id}"
        f"&season={season}"
    )

    data = requests.get(
        url,
        headers=headers
    ).json()

    standings = (
        data["response"][0]
        ["league"]
        ["standings"][0]
    )

    for team in standings:

        rank = team["rank"]
        name = team["team"]["name"]
        pts = team["points"]

        msg += (
            f"{rank}. {name} {pts}分\n"
        )

# ==================
# 世界杯比赛
# ==================

msg += "\n【世界杯】\n"

url = (
    f"https://v3.football.api-sports.io/fixtures"
    f"?league={WORLD_CUP}"
)

data = requests.get(
    url,
    headers=headers
).json()

for m in data["response"][:10]:

    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]

    msg += (
        f"{home} vs {away}\n"
    )

# ==================
# 微信推送
# ==================

push_url = (
    f"https://sctapi.ftqq.com/{sendkey}.send"
)

requests.post(
    push_url,
    data={
        "title": "⚽ 足球日报",
        "desp": msg
    }
)
```
