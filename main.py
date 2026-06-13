import os
import requests
from datetime import datetime, timedelta

from config import TEAM_IDS, WORLD_CUP
from standings import get_tables

# API KEY
api_key = os.getenv("FOOTBALL_API_KEY")

# Server酱 KEY
sendkey = os.getenv("SERVERCHAN_KEY")

headers = {
    "x-apisports-key": api_key
}

msg = ""

# =====================
# 昨天日期
# =====================

yesterday = (
    datetime.utcnow() - timedelta(days=1)
).strftime("%Y-%m-%d")

msg += "# ⚽ 昨日重点比赛\n\n"

# =====================
# 查询关注球队
# =====================

for team_name, team_id in TEAM_IDS.items():

    url = (
        "https://v3.football.api-sports.io/fixtures"
        f"?team={team_id}&date={yesterday}"
    )

    data = requests.get(
        url,
        headers=headers
    ).json()

    if "response" not in data:
        continue

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

        # 查询进球事件
        event_url = (
            "https://v3.football.api-sports.io/fixtures/events"
            f"?fixture={fixture_id}"
        )

        event_data = requests.get(
            event_url,
            headers=headers
        ).json()

        if "response" in event_data:

            for e in event_data["response"]:

                if e["type"] == "Goal":

                    player = e["player"]["name"]
                    minute = e["time"]["elapsed"]

                    msg += (
                        f"⚽ {minute}' {player}\n"
                    )

        msg += "\n"

# =====================
# 联赛积分榜
# =====================

msg += get_tables()

# =====================
# 世界杯赛程
# =====================

msg += "\n# 🌍 世界杯赛程\n\n"

url = (
    "https://v3.football.api-sports.io/fixtures"
    f"?league={WORLD_CUP}"
)

data = requests.get(
    url,
    headers=headers
).json()

if "response" in data:

    for m in data["response"][:10]:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        date = m["fixture"]["date"][:10]

        msg += (
            f"{date}\n"
            f"{home} vs {away}\n\n"
        )

# =====================
# 推送微信
# =====================

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

print("发送成功")
