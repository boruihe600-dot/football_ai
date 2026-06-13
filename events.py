import requests


def get_events(fixture_id, headers):
    """
    获取比赛事件
    """

    url = (
        f"https://v3.football.api-sports.io/fixtures/events"
        f"?fixture={fixture_id}"
    )

    response = requests.get(
        url,
        headers=headers
    )

    return response.json()
