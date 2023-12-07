import requests

while True:
    url = "https://cas.hsmob.com/cas/login/"

    querystring = {"service":"http://weekly.hsmob.com"}

    payload = {
        "username": "yuqikun",
        "password": "33333333333333333333333"
    }
    headers = {"content-type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    print(response.json())
