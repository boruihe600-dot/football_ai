import os
import requests
from datetime import datetime, timedelta
from config import TEAM_IDS, LEAGUES, WORLD_CUP

# API key
api_key = os.getenv("FOOTBALL_API_KEY")

# Server酱 key
sendkey = os.getenv("SERVERCHAN_KEY")

headers = {
    "x-apisports-key": api_key
}

msg = ""

# ======================
# 昨天日期
# ======================
yesterday = (
    datetime.utcnow() - timedelta(days=1)
).strftime("%Y-%m-%d")

msg += "# ⚽ 昨日重点比赛\n\n"

# ======================
# 查询关注球队
# ======================
for team_name, team_id in TEAM_IDS.items():

    url = (
        "https://v3.football.api-sports.io/fixtures"
        f"?team={team_id}&date={yesterday}"
    )

    data = requests.get(
        url,
        headers=headers
    ).json()

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

        for e in event_data["response"]:

            if e["type"] == "Goal":

                player = e["player"]["name"]
                minute = e["time"]["elapsed"]

                msg += (
                    f"⚽ {minute}' {player}\n"
                )

        msg += "\n"


# ======================
# 世界杯赛程
# ======================
msg += "\n# 🌎 世界杯赛程\n\n"

world_url = (
    "https://v3.football.api-sports.io/fixtures"
    f"?league={WORLD_CUP}"
)

world_data = requests.get(
    world_url,
    headers=headers
).json()

for match in world_data["response"][:10]:

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    msg += f"{home} vs {away}\n"


# ======================
# 联赛积分榜
# ======================
msg += "\n# 📊 联赛积分榜\n\n"

season = datetime.now().year

for league_name, league_id in LEAGUES.items():

    table_url = (
        "https://v3.football.api-sports.io/standings"
        f"?league={league_id}"
        f"&season={season}"
    )

    table_data = requests.get(
        table_url,
        headers=headers
    ).json()

    msg += f"\n## {league_name}\n"

    try:
        standings = (
            table_data["response"][0]
            ["league"]["standings"][0]
        )

        for team in standings:

            rank = team["rank"]
            name = team["team"]["name"]
            pts = team["points"]

            msg += (
                f"{rank}. {name} "
                f"{pts}分\n"
            )

    except:
        msg += "暂无积分榜数据\n"


# ======================
# 微信推送
# ======================
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
