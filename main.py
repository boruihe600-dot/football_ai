import os
import requests

sendkey = os.getenv("SERVERCHAN_KEY")

title = "🎉 Football AI 测试成功"
desp = "GitHub Actions 已成功运行"

url = f"https://sctapi.ftqq.com/{sendkey}.send"

data = {
    "title": title,
    "desp": desp
}

response = requests.post(url, data=data)

print(response.text)
