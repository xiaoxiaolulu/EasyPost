import re
import time

import requests

while True:
    url = "https://cas.hsmob.com/cas/login/"

    querystring = {"service": "http://weekly.hsmob.com"}

    payload = {
        "username": "qikun.yu",
        "password": "123456"
    }
    headers = {"content-type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    res = str(response.json()["userMessage"]).__contains__("账户被锁定, 冻结时间剩余")
    if res:
        print(response.json())
        time_flag = re.findall('\d+', response.json()["userMessage"])[0]
        print(time_flag)
        print(f"休息{time_flag}秒")
        time.sleep(int(time_flag))
