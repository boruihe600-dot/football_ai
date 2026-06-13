import requests

WORKER = "https://mute-dream-d2d6.boruihe600.workers.dev"

LEAGUES = {
"英超": {
"tournament": 17,
"season": 61627
},

```
"西甲": {
    "tournament": 8,
    "season": 61644
},

"中超": {
    "tournament": 649,
    "season": 70432
}
```

}

def get_tables():

```
msg = "\n# 📊 联赛积分榜\n\n"

for league_name, info in LEAGUES.items():

    msg += f"## {league_name}\n\n"

    api_url = (
        "https://api.sofascore.com/api/v1/"
        f"unique-tournament/{info['tournament']}"
        f"/season/{info['season']}"
        "/standings/total"
    )

    url = f"{WORKER}?url={api_url}"

    try:

        response = requests.get(url)

        print(response.status_code)
        print(response.text)

        data = response.json()

        rows = data["standings"][0]["rows"]

        for team in rows:

            rank = team["position"]
            name = team["team"]["name"]
            points = team["points"]

            msg += f"{rank}. {name} {points}分\n"

        msg += "\n"

    except Exception as e:

        msg += f"获取失败：{e}\n\n"

        print(e)

return msg
```
