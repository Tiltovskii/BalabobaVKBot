import json
import urllib.request
import re
from fake_useragent import UserAgent


async def zabalobobit(query, intro=1):
    user_agent = UserAgent().chrome
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agent,
        'Origin': 'https://yandex.ru',
        'Referer': 'https://yandex.ru/',
    }

    API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
    payload = {"query": query, "intro": intro, "filter": 1}
    params = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(API_URL, data=params, headers=headers)
    response = urllib.request.urlopen(req)
    text = response.read().decode('unicode-escape')
    groups = re.findall(r"(?<=[\"':])[^\"']+", text)
    text = groups[10]
    return query + ' ' + text


if __name__ == '__main__':
    user_agent = UserAgent().chrome
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agent,
        'Origin': 'https://yandex.ru',
        'Referer': 'https://yandex.ru/',
    }

    API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
    payload = {"query": "Скорпионы", "intro": 1, "filter": 1}
    params = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(API_URL, data=params, headers=headers)
    response = urllib.request.urlopen(req)
    text = response.read().decode('unicode-escape')
    print(text)
    groups = re.findall(r"(?<=[\"':])[^\"']+", text)
    query = groups[6]
    text = groups[10]
    print(query + text)
    # print(zabalobobit('привет всем'))
