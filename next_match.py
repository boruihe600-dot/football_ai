import os
import requests
from config import TEAM_IDS

api_key = os.getenv("FOOTBALL_API_KEY")

headers = {
"x-apisports-key": api_key
}

def get_next_match():

```
msg = "\n# 📅 下一场比赛\n\n"

for team_name, team_id in TEAM_IDS.items():

    url = (
        "https://v3.football.api-sports.io/fixtures"
        f"?team={team_id}"
        "&next=1"
    )

    data = requests.get(
        url,
        headers=headers
    ).json()

    if "response" not in data:
        continue

    if len(data["response"]) == 0:
        continue

    match = data["response"][0]

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    league = match["league"]["name"]

    date = match["fixture"]["date"][:10]

    msg += (
        f"## {team_name}\n"
        f"{date}\n"
        f"{home} vs {away}\n"
        f"{league}\n\n"
    )

return msg
```
