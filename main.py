import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import TEAM_IDS, WORLD_CUP

# API KEY
api_key = os.getenv("FOOTBALL_API_KEY")

# Server酱
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

                msg += f"⚽ {minute}' {player}\n"

        msg += "\n"

# ===================================
# 联赛积分榜（实时网页）
# ===================================

msg += "\n# 📊 联赛积分榜\n"

TABLE_URLS = {

    "英超":
    "https://www.espn.com/soccer/standings/_/league/eng.1",

    "西甲":
    "https://www.espn.com/soccer/standings/_/league/esp.1",

    "中超":
    "https://www.espn.com/soccer/standings/_/league/chn.1"

}

for league_name, url in TABLE_URLS.items():

    msg += f"\n## {league_name}\n"

    try:

        html = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        ).text

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        rows = soup.find_all("tr")

        count = 0

        for row in rows:

            text = row.get_text(
                " ",
                strip=True
            )

            if len(text) < 10:
                continue

            msg += text + "\n"

            count += 1

            if count >= 20:
                break

    except:

        msg += "获取失败\n"

# ===================================
# 世界杯赛程
# ===================================

msg += "\n# 🌍 世界杯赛程\n\n"

url = (
    "https://v3.football.api-sports.io/fixtures"
    f"?league={WORLD_CUP}"
)

data = requests.get(
    url,
    headers=headers
).json()

for m in data["response"][:10]:

    home = m["teams"]["home"]["name"]
    away = m["teams"]["away"]["name"]

    date = m["fixture"]["date"][:10]

    msg += (
        f"{date}\n"
        f"{home} vs {away}\n\n"
    )

# ===================================
# 推送微信
# ===================================

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
