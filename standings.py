```python
def get_tables():

    msg = "\n# 📊 联赛积分榜\n\n"

    # 英超
    msg += "## 英超\n\n"

    premier_league = [
        "阿森纳",
        "曼城",
        "曼联",
        "阿斯顿维拉",
        "利物浦",
        "伯恩茅斯",
        "桑德兰",
        "布莱顿",
        "布伦特福德",
        "切尔西",
        "富勒姆",
        "纽卡斯尔联",
        "埃弗顿",
        "利兹联",
        "水晶宫",
        "诺丁汉森林",
        "热刺",
        "西汉姆联",
        "伯恩利",
        "狼队"
    ]

    for i, team in enumerate(premier_league, start=1):
        msg += f"{i}. {team}\n"

    msg += "\n"

    # 西甲
    msg += "## 西甲\n\n"

    la_liga = [
        "巴塞罗那",
        "皇家马德里",
        "比利亚雷亚尔",
        "马德里竞技",
        "皇家贝蒂斯",
        "塞尔塔",
        "赫塔菲",
        "巴列卡诺",
        "瓦伦西亚",
        "皇家社会",
        "西班牙人",
        "毕尔巴鄂竞技",
        "塞维利亚",
        "阿拉维斯",
        "埃尔切",
        "莱万特",
        "奥萨苏纳",
        "马略卡",
        "赫罗纳",
        "皇家奥维耶多"
    ]

    for i, team in enumerate(la_liga, start=1):
        msg += f"{i}. {team}\n"

    msg += "\n"

    # 中超
    msg += "## 中超\n\n"

    chinese_super_league = [
        "上海申花",
        "成都蓉城",
        "北京国安",
        "上海海港",
        "山东泰山",
        "天津津门虎",
        "浙江队",
        "河南队",
        "武汉三镇",
        "青岛西海岸",
        "云南玉昆",
        "深圳新鹏城",
        "梅州客家",
        "长春亚泰",
        "大连英博",
        "青岛海牛"
    ]

    for i, team in enumerate(chinese_super_league, start=1):
        msg += f"{i}. {team}\n"

    msg += "\n"

    return msg
```
