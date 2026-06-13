from team_names import TEAM_NAMES


def translate_team(name):

    if name in TEAM_NAMES:
        return TEAM_NAMES[name]

    # 字典里没有
    return name
