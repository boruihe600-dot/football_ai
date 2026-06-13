import requests
from bs4 import BeautifulSoup
from translator import translate_team

TABLE_URLS = {
    "英超": "https://www.espn.com/soccer/standings/_/league/eng.1",
    "西甲": "https://www.espn.com/soccer/standings/_/league/esp.1",
    "中超": "https://www.espn.com/soccer/standings/_/league/chn.1"
}


def get_tables():

    msg = "\n# 📊 联赛积分榜\n\n"

    for league_name, url in TABLE_URLS.items():

        msg += f"## {league_name}\n\n"

        try:

            html = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            ).text

            soup = BeautifulSoup(html, "html.parser")

            rows = soup.find_all("tr")

            rank = 1

            for row in rows:

                text = row.get_text(" ", strip=True)

                if len(text) < 10:
                    continue

                # 去掉过长的数据行
                if len(text) > 80:
                    continue

                msg += f"{rank}. {text}\n"

                rank += 1

                if rank > 20:
                    break

            team_name = text

team_name = translate_team(team_name)

msg += f"{rank}. {team_name}\n"
            
        except Exception as e:

            msg += "获取失败\n\n"

    return msg
```
