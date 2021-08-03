#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import gzip
import time
from urllib import request, parse


class HttpRequest2:
    def REQ(self, url, params=None, headers=None):
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

    # 检查消息是否包含敏感词

    def censor_msg(self, censor_url, msg):
        reason_type_dict = {
            1: '暴恐违禁',
            2: '文本色情',
            3: '政治敏感',
            4: '恶意推广',
            5: '低俗辱骂',
            6: '恶意推广-联系方式',
            7: '恶意推广-软文推广',
            8: '广告法审核',
            100: '触发默认违规词库'
        }
        params = {'content': msg}
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        return_dict = {}
        res = self.REQ(censor_url, params, headers)
        return_dict['code'] = res['errcode']
        if res['errcode'] == 0:
            result = res['result']
            return_dict['is_pass'] = True if result['conclusionType'] == 1 else False
            return_dict['reason'] = []
            for hit in result['hits']:
                return_dict['reason'].append(reason_type_dict[hit['type']])
            return_dict['reason'] = '、'.join(
                reason for reason in return_dict['reason'])
        return return_dict

    # 频繁了，缓5秒
    def delay_censor_msg(self, censor_url, msg):
        res = self.censor_msg(censor_url, msg)
        if res['code'] != 0:
            print('违规词检查接口频繁了，缓5秒')
            time.sleep(5)
            return self.censor_msg(censor_url, msg)
        return res


# url = 'https://www.coder.work/textcensoring/getresult'
# res = censor_msg(url, '18703636879')
# print(res)
# print(type(res))

# res = censor_msg(url, '色比，鸡巴')
# print(res)
# print(type(res))


# url = 'http://openapi.tuling123.com/openapi/api/v2'
# data = {
#     "reqType": 0,
#     "perception": {
#         "inputText": {
#             "text": "你好"
#         },
#         "inputImage": {
#             "url": ""
#         },
#         "inputMedia": {
#             "url": ""
#         },
#         "selfInfo": {
#             "location": {
#                 "city": "上海",
#                 "province": "",
#                             "street": ""
#             }
#         }
#     },
#     "userInfo": {
#         "apiKey": "1711cee3bc1447b09969f0aa7a5fd14c",
#         "userId": "299078"
#     }
# }
# headers = {'Content-Type': 'application/json; charset=utf-8'}

# print(type(data))
# print(data['perception']['inputText']['text'])
# data['perception']['inputText']['text'] = '在干嘛？'
# res = REQ(url, data, headers)
# print(type(res))
# print(res)
