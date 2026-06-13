from team_names import TEAM_NAMES
from deep_translator import GoogleTranslator


def translate_team(name):

    if name in TEAM_NAMES:
        return TEAM_NAMES[name]

    try:
        cn = GoogleTranslator(
            source='auto',
            target='zh-CN'
        ).translate(name)

        return cn

    except:

        return name
