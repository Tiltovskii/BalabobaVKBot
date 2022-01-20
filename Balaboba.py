import json
import urllib.request
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
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    json_file = json.loads(data.decode(encoding))
    return query + ' ' + json_file['text']


