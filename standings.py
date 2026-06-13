import os
import requests

API_KEY = os.getenv("FOOTBALL_DATA_KEY")

headers = {
    "X-Auth-Token": API_KEY
}

LEAGUES = {
    "英超": "PL",
    "西甲": "PD",
    "中超": "CSL"
}


def get_tables():

    msg = "\n# 📊 联赛积分榜\n\n"

    for league_name, code in LEAGUES.items():

        msg += f"## {league_name}\n\n"

        url = (
            f"https://api.football-data.org/v4/competitions/{code}/standings"
        )

        try:

            response = requests.get(
                url,
                headers=headers
            )

            data = response.json()

            rows = data["standings"][0]["table"]

            for team in rows:

                rank = team["position"]
                name = team["team"]["shortName"]
                points = team["points"]

                msg += (
                    f"{rank}. {name} {points}分\n"
                )

            msg += "\n"

        except Exception as e:

            print(e)

            msg += (
                f"获取失败：{e}\n\n"
            )

    return msg
