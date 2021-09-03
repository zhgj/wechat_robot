#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
import random
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

    def define_msg_is_pass(self, result):
        hits = result['hits']
        for hit in hits:
            if len(hit['word_array']) > 0:
                return False
        return True

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
        # headers = {'Content-Type': 'application/json; charset=utf-8'}
        # headers = {'Host': 'www.coder.work',
        #            'Connection': 'keep-alive',
        #            'Content-Length': '51',
        #            'sec-ch-ua': '''"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"''',
        #            'Accept': 'application/json, text/javascript, */*; q=0.01',
        #            'DNT': '1',
        #            'X-Requested-With': 'XMLHttpRequest',
        #            'sec-ch-ua-mobile': '?0',
        #            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62',
        #            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #            'Origin': 'https://www.coder.work',
        #            'Sec-Fetch-Site': 'same-origin',
        #            'Sec-Fetch-Mode': 'cors',
        #            'Sec-Fetch-Dest': 'empty',
        #            'Referer': 'https://www.coder.work/textcensoring',
        #            'Accept-Encoding': 'gzip, deflate, br',
        #            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        #            'Cookie': 'Hm_lvt_1230496a24f886be1982e4b1d17d9884=1621580125; Hm_lvt_d26f2298d3a7fe583e547d2101e22936=1627817825,1627874937,1627898091,1628054001; Hm_lpvt_d26f2298d3a7fe583e547d2101e22936=1628054468'}
        headers = {'Host': 'www.coder.work',
                   'Connection': 'keep-alive',
                   'sec-ch-ua': '''"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"''',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'DNT': '1',
                   'X-Requested-With': 'XMLHttpRequest',
                   'sec-ch-ua-mobile': '?0',
                   'User-Agent': random.choice(('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73')),
                   'Content-Type': 'application/json; charset=UTF-8',
                   'Origin': 'https://www.coder.work',
                   'Sec-Fetch-Site': 'same-origin',
                   'Sec-Fetch-Mode': 'cors',
                   'Sec-Fetch-Dest': 'empty',
                   'Referer': 'https://www.coder.work/textcensoring',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                   'Cookie': random.choice(('Hm_lvt_1230496a24f886be1982e4b1d17d9884=1621580125; Hm_lvt_d26f2298d3a7fe583e547d2101e22936=1627817825,1627874937,1627898091,1628054001; Hm_lpvt_d26f2298d3a7fe583e547d2101e22936=1628054468', 'Hm_lvt_1230496a24f886be1982e4b1d17d9884=1621580125; zrCookie=814997469; Hm_lvt_9cc074900445f1842472986022b3fd60=1628757172,1629183629; Hm_lvt_d26f2298d3a7fe583e547d2101e22936=1628756216,1629179941,1629182889,1629249848; Hm_lpvt_d26f2298d3a7fe583e547d2101e22936=1629249850', 'Hm_lvt_1230496a24f886be1982e4b1d17d9884=1621580125; zrCookie=814997469; Hm_lvt_9cc074900445f1842472986022b3fd60=1628757172,1629183629; Hm_lvt_d26f2298d3a7fe583e547d2101e22936=1628756216,1629179941,1629182889,1629249848; Hm_lpvt_d26f2298d3a7fe583e547d2101e22936=1629250656', 'Hm_lvt_1230496a24f886be1982e4b1d17d9884=1621580125; zrCookie=814997469; Hm_lvt_9cc074900445f1842472986022b3fd60=1628757172,1629183629; Hm_lvt_d26f2298d3a7fe583e547d2101e22936=1628756216,1629179941,1629182889,1629249848; Hm_lpvt_d26f2298d3a7fe583e547d2101e22936=1629250741', 'Hm_lvt_1230496a24f886be1982e4b1d17d9884=1621580125; zrCookie=814997469; Hm_lvt_9cc074900445f1842472986022b3fd60=1628757172,1629183629; Hm_lvt_d26f2298d3a7fe583e547d2101e22936=1628756216,1629179941,1629182889,1629249848; Hm_lpvt_d26f2298d3a7fe583e547d2101e22936=1629250832'))}
        return_dict = {}
        try:
            res = self.REQ(censor_url, params, headers)
            return_dict['code'] = res['errcode']
        except Exception as e:
            print('违规词检查接口请求出现了异常：{0}'.format(e))
            return_dict['code'] = -1
        if return_dict['code'] == 0:
            result = res['result']
            # return_dict['is_pass'] = True if result['conclusionType'] != 2 else False
            return_dict['is_pass'] = self.define_msg_is_pass(result)
            if return_dict['is_pass'] == False:
                print(res)
            return_dict['reason'] = []
            for hit in result['hits']:
                return_dict['reason'].append(reason_type_dict[hit['type']])
            return_dict['reason'] = '、'.join(
                reason for reason in return_dict['reason'])
        return return_dict

    # 频繁了，缓5秒
    def delay_censor_msg(self, censor_url, msg):
        # return {'code': 0, 'is_pass': True, 'reason': ''}
        now = datetime.now()
        res = self.censor_msg(censor_url, msg)
        now2 = datetime.now()
        print('违规词检查耗时：' + str((now2 - now).total_seconds()))
        if res['code'] != 0:
            print('\n违规词检查接口频繁了，缓5秒')
            time.sleep(5)
            res = self.censor_msg(censor_url, msg)
            if res['code'] != 0:
                return {'code': 0, 'is_pass': True}
        return res


# url = 'https://www.coder.work/textcensoring/getresult'
# res = HttpRequest2().censor_msg(url, '18703636879')
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
