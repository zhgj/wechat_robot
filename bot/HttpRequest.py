import requests
import json
import random
from langconv import *


class HttpRequest:
    # 转换繁体到简体
    def cht_to_chs(self, line):
        line = Converter('zh-hans').convert(line)
        line.encode('utf-8')
        return line
    # 转换简体到繁体
    def chs_to_cht(self, line):
        line = Converter('zh-hant').convert(line)
        line.encode('utf-8')
        return line
    # 发送http请求
    def http_request(self, url, http_method, params=None):
        res = ''
        if http_method.upper() == 'POST':
            try:
                res = requests.post(url, params)
                print("正在进行post请求")
            except Exception as e:
                print("post请求出现了异常：{0}".format(e))
        elif http_method.upper() == 'GET':
            try:
                res = requests.post(url)
                print("正在进行get请求")
            except Exception as e:
                print("get请求出现了异常：{0}".format(e))
        return res
    # 保存gif
    def save_gif(self, path_dir, gif_uri):
        res = self.http_request(gif_uri, 'get')
        if res != '':
            # s = "abc,,,fefdaf,,,123fad,,fsdfa,,,"
            # [x for x in s.split(',') if x]
            # ['abc', 'fefdaf', '123fad', 'fsdfa']
            # 相当于以下代码：
            # for x in url2.split('/'):
            #     if x:
            #         print(x)

            # url_split = [x for x in gif_uri.split('/') if x]
            # length = len(url_split)
            # file_name = url_split[length - 1] if '.gif' in url_split[length - 1] else url_split[length - 1] + '.gif'
            # file_path = path_dir + '\\' + file_name
            file_path = path_dir + '\\gif.gif'
            with open(file_path, 'wb') as f:
                f.write(requests.get(gif_uri).content)
            res = file_path
        return res
    # 保存iciba每日音频和图片
    def save_iciba_mp3_and_img(self, path_dir, iciba_url):
        res = self.http_request(iciba_url, 'get')
        # mp3_file_path = ''
        # img_file_path = ''
        if res != '':
            iciba_info = res.json()
            filename = iciba_info['dateline'] + '_' + iciba_info['note']
            mp3_file_path = path_dir + '\\' + filename + '.mp3'
            with open(mp3_file_path, 'wb') as f:
                f.write(requests.get(iciba_info['tts']).content)
            img_file_path = path_dir + '\\' + filename +'.png'
            with open(img_file_path, 'wb') as f:
                f.write(requests.get(iciba_info['fenxiang_img']).content)
        return mp3_file_path, img_file_path

    # 获取API聊天机器人回复内容
    def bot_reply(self, bot_url, bot_url2, msg):
        msg = self.cht_to_chs(msg)
        if '笑话' in msg:
            if '笑话分类' in msg:
                return self.bot1_reply(bot_url, msg)
            bot1_joke_type = {
                                1:'夫妻',
                                2:'恶心',
                                3:'爱情',
                                4:'恐怖',
                                5:'家庭',
                                6:'校园',
                                7:'名著暴笑',
                                8:'儿童',
                                9:'医疗',
                                10:'愚人',
                                11:'司法',
                                12:'交通',
                                13:'交往',
                                14:'动物',
                                15:'民间',
                                16:'顺口溜',
                                17:'古代',
                                18:'经营',
                                19:'名人',
                                20:'幽默',
                                21:'搞笑歌词',
                                22:'体育',
                                23:'宗教',
                                24:'文艺',
                                25:'电脑',
                                26:'恋爱必读',
                                27:'英语',
                                28:'原创',
                                29:'综合',
                                30:'求爱秘籍'
                            }
            for key, value in bot1_joke_type.items():
                if value in msg:
                    return self.bot1_reply(bot_url, msg)
            return self.bot1_reply(bot_url, msg) if random.randint(0, 1) else self.bot2_reply(bot_url2, msg)
        elif '接龙' in msg or '灵签' in msg:
            return self.bot2_reply(bot_url2, msg)
        else:
            return self.bot1_reply(bot_url, msg)
    
    def bot2_reply(self, bot_url, msg):
        bot_res_json = {}
        if '观音灵签' == msg or '月老灵签' == msg or '财神爷灵签' == msg:
            bot_res = self.http_request(
                bot_url.format(msg), 'get')
            bot_res_json['result'] = 0
            # https://blog.csdn.net/qq_41375318/article/details/118578443
            # 通常解决中文显示问题：\\u问题
            # str.encode('utf-8').decode('unicode_escape')
            # 但格式化时，可用ensure_ascii=False解决
            # sort_keys=False，意思是不对json进行排序
            try:
                json_res = json.dumps(json.loads(bot_res.text.encode('utf-8').decode('utf-8-sig')), indent=4, sort_keys=False, ensure_ascii=False)
            except Exception as e:
                print("bot2：json.loads()出现异常：{0}".format(e))
                bot_res_json = {'result': 999, 'content': '出错啦，重试一下吧~'}
                return bot_res_json
            bot_res_json['content'] = json_res
        elif '笑话' in msg:
            bot_res = self.http_request(
                bot_url.format(msg), 'get')
            # https://blog.csdn.net/qq_41375318/article/details/118578443
            try:
                json_res = json.loads(bot_res.text.encode('utf-8').decode('utf-8-sig'))
            except Exception as e:
                print("bot2：json.loads()出现异常：{0}".format(e))
                bot_res_json = {'result': 999, 'content': '出错啦，重试一下吧~'}
                return bot_res_json
            bot_res_json['result'] = 0
            bot_res_json['content'] = json_res['title'] + '：\n' + json_res['content']
        else:
            if '接龙' in msg:
                msg = msg.replace('成语接龙', '@cy').replace('接龙', '@cy').replace(' ', '')
                bot_res = self.http_request(
                    bot_url.format(msg), 'get')
                bot_res_json['result'] = 0
                # https://blog.csdn.net/qq_41375318/article/details/118578443
                bot_res_json['content'] = bot_res.text.encode('utf-8').decode('utf-8-sig')
        return bot_res_json
    
    def bot1_reply(self, bot_url, msg):
        bot_res = self.http_request(
            bot_url.format(msg), 'get')
        try:
            bot_res_json = bot_res.json()
        except Exception as e:
            print("bot1_res.json()出现异常：{0}".format(e))
            bot_res_json = {'result': 999, 'content': '出错啦，重试一下吧~'}
            return bot_res_json
        print(bot_res_json)
        bot_res_json['content'] = bot_res_json['content'].replace('{br}', '\n')
        bot_res_json['content'] = bot_res_json['content'].split(
            '}', 1)[1] if '}' in bot_res_json['content'] else bot_res_json['content']
        # print(bot_res_json)
        bot_res_json['content'] = self.cht_to_chs(
            bot_res_json['content']).replace('菲菲', '我')
        # print(bot_res_json)
        return bot_res_json


# if __name__ == '__main__':
#     base_dir = r'C:\Users\zhanggaojiong\Downloads\wechat_pc_api-master\bot'
#     iciba_path_dir = base_dir + r'\iciba'
#     url = 'http://open.iciba.com/dsapi/'
#     res = HttpRequest().save_iciba_mp3_and_img(iciba_path_dir, url)
#     print(res)
#     print(type(res))

# if __name__ == '__main__':
#     url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={0}'
#     url2 = 'http://i.itpk.cn/api.php?question={0}'
#     res = HttpRequest().bot_reply(url, url2, '笑话')
#     print(res)
#     print(type(res))
#     print(type(res.json()))
#     print(res.json())

# if __name__ == '__main__':
#     url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=你好'
#     res = HttpRequest().http_request(url, 'get')
#     print(type(res))
#     print(type(res.json()))
#     print(res.json())

# https://www.sojson.com/api/semantic.html
# eg:
# response:{"result":0,"content":"曲项向天歌"}


# if __name__ == '__main__':

#     url = 'http://wxapp.tc.qq.com/262/20304/stodownload?m=41d08ccd657577d4c18253ac17fa7067&amp;filekey=30350201010421301f020201060402535a041041d08ccd657577d4c18253ac17fa7067020301aa4b040d00000004627466730000000131&amp;hy=SZ&amp;storeid=32303231303632353137323434343030303063363036336564336538346262633338356630393030303030313036&amp;bizid=1023'

#     url2 = 'http://emoji.qpic.cn/wx_emoji/8xdicpwlE36hDfmr8vPBHcQIt5yzUUDwxyPwgVrXDaIBWB7g43ic4I1g/'

#     url3 = 'http://ww4.sinaimg.cn/large/a7bf601fjw1f7jsbj34a1g20kc0bdnph.gif'

#     path_dir = r'C:\Users\zhanggaojiong\Downloads\wechat_pc_api-master\bot\gif'

#     res = HttpRequest().http_request(url2, 'get')
#     if res != '':
#         # s = "abc,,,fefdaf,,,123fad,,fsdfa,,,"
#         # [x for x in s.split(',') if x]
#         # ['abc', 'fefdaf', '123fad', 'fsdfa']
#         for x in url2.split('/'):
#             if x:
#                 print(x)
#         url_split = [x for x in url2.split('/') if x]
#         len = len(url_split)
#         file_name = url_split[len - 1] if '.gif' in url_split[len - 1] else url_split[len - 1]+'.gif'
#         file_path = path_dir + '\\' + file_name
#         with open(file_path, 'wb') as f:
#             f.write(requests.get(url2).content)

# path_dir = r'C:\Users\zhanggaojiong\Downloads\wechat_pc_api-master\bot\gif'
# url = 'http://wxapp.tc.qq.com/262/20304/stodownload?m=41d08ccd657577d4c18253ac17fa7067&amp;filekey=30350201010421301f020201060402535a041041d08ccd657577d4c18253ac17fa7067020301aa4b040d00000004627466730000000131&amp;hy=SZ&amp;storeid=32303231303632353137323434343030303063363036336564336538346262633338356630393030303030313036&amp;bizid=1023'
# url2 = 'http://emoji.qpic.cn/wx_emoji/8xdicpwlE36hDfmr8vPBHcQIt5yzUUDwxyPwgVrXDaIBWB7g43ic4I1g/'

# request = HttpRequest()
# request.save_gif(path_dir, url)

# url3 = 'http://wxapp.tc.qq.com/262/20304/stodownload?m=f4d75fc67ffa7ea796ead59d620550ec&filekey=30350201010421301f020201060402535a0410f4d75fc67ffa7ea796ead59d620550ec0203011cae040d00000004627466730000000131&hy=SZ&storeid=32303231303632343233303333343030306365366531336263353062383430333064356630393030303030313036&bizid=1023'
# HttpRequest().save_gif(path_dir, url3)
