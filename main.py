import os
import requests
from datetime import datetime, timedelta
from config import TEAM_IDS, LEAGUES, WORLD_CUP

api_key = os.getenv("FOOTBALL_API_KEY")
sendkey = os.getenv("SERVERCHAN_KEY")

headers = {
    "x-apisports-key": api_key
}

msg = ""

# ==================
# 昨天日期
# ==================
yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

msg += "# ⚽ 昨日重点比赛\n\n"

# ==================
# 查询关注球队
# ==================
for team_name, team_id in TEAM_IDS.items():

    url = (
        f"https://v3.football.api-sports.io/fixtures"
        f"?team={team_id}&date={yesterday}"
    )

    r = requests.get(url, headers=headers)
    data = r.json()

    if len(data["response"]) == 0:
        continue

    for match in data["response"]:

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        goals_home = match["goals"]["home"]
        goals_away = match["goals"]["away"]

        msg += (
            f"## {home} {goals_home}-{goals_away} {away}\n"
        )

        fixture_id = match["fixture"]["id"]

        # 查询事件
        event_url = (
            f"https://v3.football.api-sports.io/fixtures/events"
            f"?fixture={fixture_id}"
        )

        event_data = requests.get(
            event_url,
            headers=headers
        ).json()

        for e in event_data["response"]:

            if e["type"] == "Goal":

                player = e["player"]["name"]
                minute = e["time"]["elapsed"]

                msg += (
                    f"⚽ {minute}' {player}\n"
                )

        msg += "\n"
