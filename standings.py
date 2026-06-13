import requests
from bs4 import BeautifulSoup

TABLE_URLS = {
    "英超": "https://www.espn.com/soccer/standings/_/league/eng.1",
    "西甲": "https://www.espn.com/soccer/standings/_/league/esp.1",
    "中超": "https://www.espn.com/soccer/standings/_/league/chn.1"
}

def get_tables():

    msg = "\n# 📊 联赛积分榜\n\n"

    for league_name, url in TABLE_URLS.items():

        msg += f"## {league_name}\n"

        try:

            html = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            ).text

            soup = BeautifulSoup(html, "html.parser")

            rows = soup.find_all("tr")

            count = 0

            for row in rows:

                text = row.get_text(" ", strip=True)

                if len(text) < 10:
                    continue

                msg += text + "\n"

                count += 1

                if count >= 20:
                    break

            msg += "\n"

        except:

            msg += "获取失败\n"

    return msg
