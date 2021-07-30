#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import gzip
from urllib import request, parse


def REQ(url, params=None, headers=None):
    headers = headers or {}
    if params:  # dict
        params = json.dumps(
            params) if headers['Content-Type'] and 'application/json' in headers['Content-Type'] else parse.urlencode(params)
        params = params.encode('utf-8')

    # 当 params 不为空，method 为 POST
    req = request.Request(url, params, headers)
    with request.urlopen(req, timeout=60) as page:
        res = page.read()

        if page.getheader('Content-Encoding') == 'gzip':
            res = gzip.decompress(res).decode('utf-8')
        else:
            res = res.decode('utf-8')

        if 'application/json' in page.getheader('Content-Type'):
            res = json.loads(res)

        return res


url = 'http://openapi.tuling123.com/openapi/api/v2'
data = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": "你好"
        },
        "inputImage": {
            "url": ""
        },
        "inputMedia": {
            "url": ""
        },
        "selfInfo": {
            "location": {
                "city": "上海",
                "province": "",
                            "street": ""
            }
        }
    },
    "userInfo": {
        "apiKey": "1711cee3bc1447b09969f0aa7a5fd14c",
        "userId": "299078"
    }
}
headers = {'Content-Type': 'application/json; charset=utf-8'}

print(type(data))
print(data['perception']['inputText']['text'])
data['perception']['inputText']['text'] = '在干嘛？'
res = REQ(url, data, headers)
print(type(res))
print(res)
