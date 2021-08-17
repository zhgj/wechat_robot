# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wechat
import json
import time
import random
import logging
from wechat import WeChatManager, MessageType
from queue import Queue
from HttpRequest import HttpRequest
from HttpRequest2 import HttpRequest2
from RawMsg import RawMsg
from UserInfo import UserInfo
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from time_nlp.TimeNormalizer import TimeNormalizer
from datetime import datetime, timedelta
from message.NextReply import *
from Dat2Img import *
from hubserving import *


wechat_manager = WeChatManager(libs_path='../libs')

# logging.basicConfig(level=logging.ERROR)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

bot_wxid = 'wxid_hzwhlf2n3om121'
my_wxid = 'zhanggaojiong'
# bot_wxid = 'zhanggaojiong'
# my_wxid = 'wxid_hzwhlf2n3om121'

# 群消息互转
# 格式：'romm_wxid1','romm_wxid1文本消息转出前缀','room_wxid2','room_wxid2文本消息转出前缀'
exchange_msg_room_wxid = {
    # 1: ['5134159600@chatroom', '', '5104481030@chatroom', ''],
    2: ['6361490023@chatroom', '[1群|{0}]\n', '17948514722@chatroom', '[2群|{0}]\n'],
    3: ['19005034370@chatroom', '', '21116388962@chatroom', '']
}

# 禁止转发的关键词列表
not_exchange_key_text_list = [
    '贷款额度', '征信有问题也能', '单人面签', '无担保', '火热招募', '大礼包', '盛装亮相', '千件奖品', '任你抽', '等你抽', '等你拿', '信用贷款', '需要请联系', '集赞', '壕气', '福利'
]

# 经常需要发送的图片路径（换微信登陆发送不了）
# commom_send_picture = {
#     '物业': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\zhanggaojiong\\FileStorage\\Image\\2021-07\\eaf6f3878ad29b1e2cdafbd269cb2f0c.dat'],
#     '周口车': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\zhanggaojiong\\FileStorage\\Image\\2021-07\\42959d48fd5fa187b7148846007fc20d.dat'],
#     '水费计算': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\zhanggaojiong\\FileStorage\\Image\\2021-07\\e2919bfc16490fbc74021dbea0d492f3.dat'],
#     '天然气': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\zhanggaojiong\\FileStorage\\Image\\2021-07\\4651e200dc416cd5d62c66563929ebce.dat'],
#     '领钥匙': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\zhanggaojiong\\FileStorage\\Image\\2021-07\\fe6867bb9e73e3738f4048898e4a1c1e.dat']
# }
commom_send_picture = {
    '物业': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\wxid_hzwhlf2n3om121\\FileStorage\\Image\\2021-07\\1af6ec43a3c0f90578fde9ea4c87589a.dat'],
    '周口车': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\wxid_hzwhlf2n3om121\\FileStorage\\Image\\2021-07\\6daf1a6ec2a1a888b7e7556b5cffa03f.dat'],
    '水费计算': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\wxid_hzwhlf2n3om121\\FileStorage\\Image\\2021-07\\2dfb35a679ba423900ea8c1a40ad2fe2.dat'],
    '天然气': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\wxid_hzwhlf2n3om121\\FileStorage\\Image\\2021-07\\c0b27cb695bbc1c9ff4970645556013d.dat'],
    '领钥匙': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\wxid_hzwhlf2n3om121\\FileStorage\\Image\\2021-07\\28feb1c2a98a7d1a935700a5617d6a81.dat'],
    '打疫苗': ['C:\\Users\\zhanggaojiong\\Documents\\WeChat Files\\wxid_hzwhlf2n3om121\\FileStorage\\Image\\2021-07\\c79453aad013c863f03fe0accedc9b25.dat']
}

# 格式：[['触发条件1','触发条件2'], ['触发条件1','触发条件2'], ['消息回复类型1','消息回复类型2'], [['回复内容1', '回复内容2'], ['回复内容1', '回复内容2']]]
# 前两个条件and；
reply_msg_type = {
    '收破烂电话': [['破烂', '纸箱', '废品'], ['电话', '号码', '联系方式'], ['text'], [['\n都是群里以前发的，不保证可用，可以试试，如果不能用了群里说一下\n', '18439451096', '18135751786', '13403851362', '15224993425', '13193600443', '15703890422']]],
    '所谓物业': [['物业', '修电梯', '领钥匙', '验房', '充电', '水厂', '售楼部', '电工'], ['电话', '号码', '联系方式', '找谁'], ['text', 'picture'], [['大门口值班室拍的，不知道还有用不'], commom_send_picture['物业']]],
    '张宏电话': [['张红', '张宏', '张洪', '张弘', '张的', '张会计'], ['电话', '号码', '联系方式'], ['text'], [['13525778772']]],
    '马晨电话': [['马晨'], ['电话', '号码', '联系方式'], ['text'], [['18939496262']]],
    '周口车电话': [['周口'], ['电话', '号码', '联系方式', '车'], ['text', 'picture'], [['\n都是群里以前发的，不保证可用，可以试试，如果不能用了群里说一下\n', '13949997920', '15516777066', '13673864370', '18438168828', '13253773308', '17796530101', '18736108761'], commom_send_picture['周口车']]],
    '淮阳车电话': [['淮阳'], ['电话', '号码', '联系方式', '车'], ['text'], [['\n都是群里以前发的，不保证可用，可以试试，如果不能用了群里说一下\n', '13949997920', '15896799837', '15138363087']]],
    '漯河车电话': [['漯河'], ['电话', '号码', '联系方式', '车'], ['text'], [['\n都是群里以前发的，不保证可用，可以试试，如果不能用了群里说一下\n', '17657586111', '17329261181', '17329277977', '19939481799']]],
    '周口天气': [['老家', '今天', '周口', '项城', '明天'], ['天气', '雨', '雪', '风'], ['text'], [['周口天气']]],
    '水费问题': [['水费'], ['咋算', '阶梯', '计算'], ['text', 'picture'], [['水费是按阶梯的，一个月只有8吨按3.5算的，微信支付宝都可以交'], commom_send_picture['水费计算']]],
    '电费问题': [['电费'], ['咋算', '如何算', '多钱', '多少钱', '去哪'], ['text'], [['500块钱充880度，算下来一度是：0.5681818...。电只能在售楼部交，卡里有应急的10度电']]],
    '天然气问题': [['燃气', '天然气'], ['去哪', '在哪', '电话', '号码', '联系方式', '网上'], ['text', 'picture'], [['\n平安大道(老环城路)与富民路交叉路口往东南约90米', '红旗学校斜对面吧，这几个电话你试试吧，问一下', '(0394)4281234', '绑定卡号，手机上也可以缴费', '第一次需要去营业厅，以后就不用了'], commom_send_picture['天然气']]],
    '领钥匙': [['领钥匙', '拿钥匙'], ['钱', '收', '要', '交'], ['text', 'picture'], [['\n这是一位业主以前领钥匙的收费单，装修保证金现在收2000了'], commom_send_picture['领钥匙']]],
    '抄水表': [['抄水表', '抄表'], ['电话', '号码', '联系方式', '微信'], ['text', 'card'], [['这是抄水表马瑞的微信'], ['wxid_armkfcrcpwvc12']]],
    '打疫苗': [['疫苗'], ['去哪', '在哪', '分哪'], ['text', 'picture'], [['''\n7月10日起，项城市群众接种新冠疫苗将根据身份证居住地址，按辖区开展接种工作，具体分为四个接种点：
水寨卫生院负责水寨街道、官会镇、高寺镇、李寨镇。
城郊卫生院负责花园街道、光武街道、南顿镇、范集镇、永丰镇、三店镇、孙店镇。
秣陵卫生院负责秣陵镇、贾岭镇、付集镇、新桥镇。
卫校负责莲花街道、东方街道、千佛阁街道、郑郭镇、王明口镇、丁集镇。
 
 
项城市疫情防控指挥部办公室
2021年7月9日''', '''\n\n通知
各位支部书记：
        接市疫情防控指挥部通知，从明天7月18日开始，千佛阁疫苗接种点接种第一针疫苗。
       接种范围：15—17岁青少年及60岁以上的老年人。
       接种地点：千佛阁派出所南侧千佛阁卫生服务中心新址。
       要求各社区支部书记，立即组织社区干部，依据本次接种年龄段，对本社区青少年、老人逐街道、逐小区、逐户通知，做到社区不漏户、户不漏人。'''], commom_send_picture['打疫苗']]]
}
# 不需要机器人回复消息的人员列表
not_reply_list = ['wxid_d0xb5fea91xo21',  # 璐璐
                  'wxid_52x8hjwxfzgi22',
                  'wxid_itbbswvx2hq622',
                  'huhu390776',  # 胡
                  'dreamfinding',  # 袁
                  'shijianping440180',  # 施
                  'tonychi',  # 齐
                  'wxid_w5mz93wdgacp22',  # 钱进
                  'wxid_44q6kw082lja22',  # 余军
                  'wxid_pp82s9d2koxr12',  # 张浩
                  'wxid_k66q8l9wzw0r',  # 宏扬 宋
                  'sky6498480',  # 三部 王磊
                  'MAKIwen0207',  # 人事 许
                  'wxid_43p384wu6vhi22',  # 王玲
                  '18078033692@chatroom',  # 海天信息提供
                  '2341491378@chatroom',  # 一家人
                  '1310294697@chatroom'  # 家、永远是我们
                  '18885712152@chatroom',  # 郑州营收
                  '3595016270@chatroom',  # 研发部
                  '24239987929@chatroom',  # 3H-中山远传
                  '20868992414@chatroom',  # 中山公用水务群(肯特流量计)
                  '25015978703@chatroom',  # 中山公用与常德nb
                  '20580597839@chatroom',  # 奉贤水表数据沟通群
                  '5486880221@chatroom',  # 统一使用新通讯协议
                  '18035020979@chatroom',  # 西海岸水务自研协议开发交流群
                  '18421931893@chatroom',  # 积成远传设备调试交流
                  '17882530434@chatroom',  # 易维远传设备交流群
                  '2654691168@chatroom',  # 三高大家庭
                  '21602913425@chatroom']  # 清美

iciba_everyday_remind_list = [my_wxid]
# 各种消息的缓存队列
msg_text_queue = Queue()
msg_picture_queue = Queue()
msg_voice_queue = Queue()
msg_video_queue = Queue()
msg_file_queue = Queue()
msg_link_queue = Queue()
msg_emoji_queue = Queue()
msg_sys_queue = Queue()
msg_pay_queue = Queue()
msg_miniapp_queue = Queue()
msg_other_app_queue = Queue()

remind_queue = Queue()
wechat_client_id = None
# 存储拉取的群列表
# base_dir = r'D:\Downloads\wechat_pc_api-master\bot'
base_dir = r'C:\Users\zhanggaojiong\Downloads\wechat_pc_api-master\bot'
group_info_path = base_dir + r'\json_info\chatrooms.json'
friend_info_path = base_dir + r'\json_info\friends.json'
gif_path_dir = base_dir + r'\gif'
iciba_path_dir = base_dir + r'\iciba'
group1_info_path = base_dir + r'\json_info\group1.json'
group2_info_path = base_dir + r'\json_info\group2.json'

request = HttpRequest()
request2 = HttpRequest2()
rawmsg = RawMsg()
userinfo = UserInfo()
# api机器人地址
bot_url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={0}'
bot_url2 = 'http://i.itpk.cn/api.php?question={0}'
# iciba每日一词
iciba_url = 'http://open.iciba.com/dsapi/'
# 违规词检查
censor_url = 'https://www.coder.work/textcensoring/getresult'
# OCR识别url
ocr_url = 'http://127.0.0.1:9890/predict/ocr_system'
# 图像识别开关
ocr_switch = True

# gif是否能发送


def gif_is_can_send(raw_msg):
    gif_info = rawmsg.get_gif_msg_info(raw_msg)
    cdnurl = gif_info['cdnurl']
    print(cdnurl)
    file_path = request.save_gif(gif_path_dir, cdnurl)
    return file_path

# 群聊内容监测，按内容回复


def bot_reply_type(client_id, message_data):
    for key, value in reply_msg_type.items():
        flag = False
        for condition in value[0]:
            if condition in message_data['msg']:
                flag = True
                break
        flag2 = False
        for condition in value[1]:
            if condition in message_data['msg']:
                flag2 = True
                break
        if flag and flag2 and message_data['from_wxid'] != bot_wxid and message_data['to_wxid'] not in not_reply_list:
            for i in range(len(value[2])):
                send_type = value[2][i]
                if send_type == 'text':
                    text_join = '、'.join(value[3][i])
                    print(key + ':' + text_join)
                    if '天气' in key:
                        content = request.bot_reply(
                            bot_url, bot_url2, text_join)['content']
                    else:
                        content = key + '：' + text_join
                    wechat_manager.send_text(
                        client_id, message_data['to_wxid'], content)
                elif send_type == 'picture':
                    for url in value[3][i]:
                        print(key + ':' + url)
                        wechat_manager.send_image(
                            client_id, message_data['to_wxid'], url)
                elif send_type == 'card':
                    if bot_wxid == 'zhanggaojiong':
                        for card in value[3][i]:
                            wechat_manager.send_user_card(
                                client_id, message_data['to_wxid'], card)

# 每日iciba提醒任务


def iciba_everyday_job():
    tts_img_path = request.save_iciba_mp3_and_img(iciba_path_dir, iciba_url)
    if tts_img_path[0] == '' or tts_img_path[1] == '':
        time.sleep(5)
        tts_img_path = request.save_iciba_mp3_and_img(
            iciba_path_dir, iciba_url)
    random_second = random.randint(0, 7200)
    print('iciba_everyday_job 延迟秒数：' + str(random_second))
    time.sleep(random_second)
    for remind_wxid in iciba_everyday_remind_list:
        wechat_manager.send_image(
            wechat_client_id, remind_wxid, tts_img_path[1])
        wechat_manager.send_file(
            wechat_client_id, remind_wxid, tts_img_path[0])
    if bot_wxid != my_wxid:
        zx_wxid = 'wxid_37gktrv5yv5322'
        wechat_manager.send_image(wechat_client_id, zx_wxid, tts_img_path[1])
        wechat_manager.send_file(wechat_client_id, zx_wxid, tts_img_path[0])

# 发送提醒消息


def send_remind_text(to_wxid, text):
    wechat_manager.send_text(wechat_client_id, to_wxid, text)

# 接收提醒消息后添加待提醒任务


def add_date_job():
    while not remind_queue.empty():
        message_data = remind_queue.get()
        remind_text = '提醒'
        if remind_text in message_data['msg']:
            time_remindcontent = message_data['msg'].split(remind_text)
            time_remindcontent[1] = time_remindcontent[1].strip().replace(
                '我', '')
            if time_remindcontent[1] == '':
                wechat_manager.send_text(
                    wechat_client_id, message_data['from_wxid'], '请对我说：什么时间（多久后）提醒我干什么事')
                break
            tn = TimeNormalizer(isPreferFuture=False)
            time_remindcontent[0] = time_remindcontent[0].replace(
                '以后', '').replace('之后', '').replace('后', '')
            time_dict = tn.parse(time_remindcontent[0], datetime.now())
            timeStr = ''
            if 'error' in time_dict.keys():
                wechat_manager.send_text(
                    wechat_client_id, message_data['from_wxid'], '没理解你说的时间！换种表达方式？')
                break
            if time_dict['type'] == 'timestamp':
                timeStr = time_dict['timestamp']
            elif time_dict['type'] == 'timedelta':
                time_delta_dict = time_dict['timedelta']
                now = datetime.now()
                delta = timedelta(days=time_delta_dict['year'] * 365 + time_delta_dict['month'] * 30 + time_delta_dict['day'],
                                  hours=time_delta_dict['hour'], minutes=time_delta_dict['minute'], seconds=time_delta_dict['second'])
                timeStr = str(now + delta).split('.')[0]
            remind_time = datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            print(now)
            print(remind_time)
            if remind_time < now:
                wechat_manager.send_text(
                    wechat_client_id, message_data['from_wxid'], timeStr + '，你在逗我吗？要提醒的时间点已经过去啦！')
                break
            delta_days = (remind_time - now).days
            if delta_days > 365 * 80:
                wechat_manager.send_text(
                    wechat_client_id, message_data['from_wxid'], '超过80年？我怕你活不了那么久！')
                break
            elif delta_days > 365:
                wechat_manager.send_text(
                    wechat_client_id, message_data['from_wxid'], '超过1年了，我怕我活不了这么久！')
                break
            wechat_manager.send_text(
                wechat_client_id, message_data['from_wxid'], reply_ok(timeStr, '', True))
            remind_content = '\u23f0  ' + time_remindcontent[1]
            redis_store = RedisJobStore(
                host='localhost', port='6379', db=0, password='')
            jobstores = {'redis': redis_store}
            executors = {
                'default': ThreadPoolExecutor(10),  # 默认线程数
                'processpool': ProcessPoolExecutor(3)  # 默认进程
            }
            scheduler = BackgroundScheduler(
                jobstores=jobstores, executors=executors)
            scheduler.add_job(func=send_remind_text, args=[
                              message_data['from_wxid'], remind_content], trigger="date", next_run_time=timeStr, jobstore='redis', misfire_grace_time=60*60)
            scheduler.start()
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def add_date_job2(scheduler, message_data):
    remind_text = '提醒'
    time_remindcontent = message_data['msg'].split(remind_text)
    time_remindcontent[1] = time_remindcontent[1].strip().replace(
        '我', '')
    if time_remindcontent[1] == '':
        wechat_manager.send_text(
            wechat_client_id, message_data['from_wxid'], '请对我说：什么时间（多久后）提醒我干什么事')
        return
    tn = TimeNormalizer(isPreferFuture=False)
    time_remindcontent[0] = time_remindcontent[0].replace(
        '以后', '').replace('之后', '').replace('后', '')
    time_dict = tn.parse(time_remindcontent[0], datetime.now())
    timeStr = ''
    if 'error' in time_dict.keys():
        wechat_manager.send_text(
            wechat_client_id, message_data['from_wxid'], '没理解你说的时间！换种表达方式？')
        return
    if time_dict['type'] == 'timestamp':
        timeStr = time_dict['timestamp']
    elif time_dict['type'] == 'timedelta':
        time_delta_dict = time_dict['timedelta']
        now = datetime.now()
        delta = timedelta(days=time_delta_dict['year'] * 365 + time_delta_dict['month'] * 30 + time_delta_dict['day'],
                          hours=time_delta_dict['hour'], minutes=time_delta_dict['minute'], seconds=time_delta_dict['second'])
        timeStr = str(now + delta).split('.')[0]
    remind_time = datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    print(now)
    print(remind_time)
    if remind_time < now:
        wechat_manager.send_text(
            wechat_client_id, message_data['from_wxid'], timeStr + '，你在逗我吗？要提醒的时间点已经过去啦！')
        return
    delta_days = (remind_time - now).days
    if delta_days > 365 * 80:
        wechat_manager.send_text(
            wechat_client_id, message_data['from_wxid'], '超过80年？我怕你活不了那么久！')
        return
    elif delta_days > 365:
        wechat_manager.send_text(
            wechat_client_id, message_data['from_wxid'], '超过1年了，我怕我活不了这么久！')
        return
    wechat_manager.send_text(
        wechat_client_id, message_data['from_wxid'], reply_ok(timeStr, '', True))
    remind_content = '\u23f0  ' + time_remindcontent[1]
    scheduler.add_job(func=send_remind_text, args=[
        message_data['from_wxid'], remind_content], trigger="date", next_run_time=timeStr, jobstore='redis', misfire_grace_time=60*60)
    # scheduler.start()

# 这里测试函数回调


@wechat.CONNECT_CALLBACK(in_class=False)
def on_connect(client_id):
    print('[on_connect] client_id: {0}'.format(client_id))
    global wechat_client_id
    wechat_client_id = client_id


@wechat.RECV_CALLBACK(in_class=False)
def on_recv(client_id, message_type, message_data):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' [on_recv] client_id: {0}, message_type: {1}, message:{2}'.format(
        client_id, message_type, json.dumps(message_data, indent=4, sort_keys=True)))
    if message_type == MessageType.MT_RECV_TEXT_MSG:
        if (len([key_text for key_text in not_exchange_key_text_list if key_text in message_data['msg']])) > 0:
            pass
        else:
            msg_text_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_PICTURE_MSG:
        time.sleep(2)
        msg_picture_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_VOICE_MSG:
        print(message_type)
        # msg_voice_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_VIDEO_MSG:
        time.sleep(2)
        msg_video_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_FILE_MSG:
        time.sleep(2)
        msg_file_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_LINK_MSG:
        msg_link_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_EMOJI_MSG:
        msg_emoji_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_SYSTEM_MSG:
        msg_sys_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_WCPAY_MSG:
        msg_pay_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_MINIAPP_MSG:
        msg_miniapp_queue.put(message_data)
    elif message_type == MessageType.MT_RECV_OTHER_APP_MSG:
        msg_other_app_queue.put(message_data)
    elif message_type == MessageType.MT_DATA_FRIENDS_MSG:
        with open(friend_info_path, 'wt') as f:
            f.write(json.dumps(message_data, indent=4, sort_keys=True))
    elif message_type == MessageType.MT_DATA_CHATROOMS_MSG:
        with open(group_info_path, 'wt') as f:
            f.write(json.dumps(message_data, indent=4, sort_keys=True))
    elif message_type == MessageType.MT_DATA_CHATROOM_MEMBERS_MSG:
        print(group1_info_path)
        with open(group1_info_path, 'wt') as f:
            f.write(json.dumps(message_data, indent=4, sort_keys=True))
    else:
        print(message_type)


@wechat.CLOSE_CALLBACK(in_class=False)
def on_close(client_id):
    print('[on_close] client_id: {0}'.format(client_id))

# 这里测试类回调， 函数回调与类回调可以混合使用


class LoginTipBot(wechat.CallbackHandler):

    @wechat.RECV_CALLBACK(in_class=True)
    def on_message(self, client_id, message_type, message_data):
        # 判断登录成功后，就向文件助手发条消息
        if message_type == MessageType.MT_USER_LOGIN:
            wechat_manager.send_text(
                client_id, 'filehelper', '😂😂😂\uE052该消息通过wechat_pc_api项目接口发送')
            # print(exchange_msg_room_wxid[3][0])
            # print(exchange_msg_room_wxid[3][2])
            # print(exchange_msg_room_wxid.keys())
            # wechat_manager.send_text(client_id, exchange_msg_room_wxid[3][0], 'hi')
            # wechat_manager.send_text(client_id, exchange_msg_room_wxid[3][2], 'hi')
            # wechat_manager.send_user_card(client_id, 'wxid_hzwhlf2n3om121', 'zhaoxue18829018243')
            # wechat_manager.send_user_card(client_id, 'wxid_hzwhlf2n3om121', 'wxid_armkfcrcpwvc12')


if __name__ == "__main__":
    bot = LoginTipBot()

    # 添加回调实例对象
    wechat_manager.add_callback_handler(bot)
    wechat_manager.manager_wechat(smart=True)
    # wechat_manager.get_chatrooms(wechat_client_id)
    # wechat_manager.get_friends(wechat_client_id)
    # print(exchange_msg_room_wxid[2][2])
    # wechat_manager.get_chatroom_members(wechat_client_id, exchange_msg_room_wxid[2][0])
    # wechat_manager.get_chatroom_members(wechat_client_id, exchange_msg_room_wxid[2][2])

    # scheduler = BackgroundScheduler()
    redis_store = RedisJobStore(
        host='localhost', port='6379', db=0, password='')
    jobstores = {'redis': redis_store}
    executors = {
        'default': ThreadPoolExecutor(10),  # 默认线程数
        'processpool': ProcessPoolExecutor(3)  # 默认进程
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler(
        jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    # date: 特定的时间点触发
    # interval: 固定时间间隔触发
    # cron: 在特定时间周期性地触发
    scheduler.add_job(func=iciba_everyday_job,
                      trigger="cron", hour=6, minute=30, jobstore='redis', misfire_grace_time=2*60*60, id='iciba_everyday_job', replace_existing=True)
    scheduler.add_job(func=send_remind_text, args=[my_wxid, '\u23f0  还房贷'],
                      trigger="cron", day=9, hour=15, minute=0, start_date='2017-10-9', end_date='2032-9-10', jobstore='redis', misfire_grace_time=24*60*60, id='house_loan_everymonth_job', replace_existing=True)
    scheduler.add_job(func=send_remind_text, args=[my_wxid, '\u23f0  还车贷'],
                      trigger="cron", day=15, hour=15, minute=0, start_date='2020-9-15', end_date='2022-9-16', jobstore='redis', misfire_grace_time=24*60*60, id='car_loan_everymonth_job', replace_existing=True)
    scheduler.add_job(func=send_remind_text, args=[my_wxid, '\u23f0  交房租'],
                      trigger="cron", month='2,5,8,11', day=20, hour=15, minute=0, start_date='2020-11-20', end_date='2023-5-21', jobstore='redis', misfire_grace_time=24*60*60, id='room_charge_every3month_job', replace_existing=True)
    # scheduler.add_job(func=add_date_job, trigger="interval", seconds=1)
    # scheduler.add_job(job, 'interval', seconds=1)
    scheduler.start()

    # 阻塞主线程
    while True:
        time.sleep(0.5)
        # 测试转发图片消息
        # wechat_manager.send_image(wechat_client_id, 'filehelper', r'C:\Users\zhanggaojiong\Downloads\wechat_pc_api-master\images\微信图片_20210710231432.png')
        while not msg_sys_queue.empty():
            message_data = msg_sys_queue.get()
            if '红包' in message_data['raw_msg'] and '手机' in message_data['raw_msg']:
                wechat_manager.send_text(
                    wechat_client_id, 'filehelper', '有人发红包啦！')
                wechat_manager.send_text(wechat_client_id, my_wxid, '有人发红包啦！')

        while not msg_pay_queue.empty():
            message_data = msg_pay_queue.get()
            wechat_manager.send_text(
                wechat_client_id, 'filehelper', '有人给你转账啦！')

        while not msg_text_queue.empty():
            message_data = msg_text_queue.get()
            if '提醒' in message_data['msg'] and message_data['from_wxid'] != bot_wxid and message_data['room_wxid'] == '':
                # remind_queue.put(message_data)
                add_date_job2(scheduler, message_data)
            # print(message_data)
            # print('queue size:{0}'.format(msg_queue.qsize()))
            for key, value in exchange_msg_room_wxid.items():
                if message_data['to_wxid'] == value[0] and message_data['from_wxid'] != bot_wxid and bot_wxid not in message_data['at_user_list']:
                    res = request2.delay_censor_msg(
                        censor_url, message_data['msg'])
                    if res['is_pass']:
                        wechat_manager.send_text(wechat_client_id, value[2], (value[1] if key != 2 else value[1].format(request.cht_to_chs(
                            userinfo.get_nickname_by_wxid(group1_info_path, message_data['from_wxid'])))) + message_data['msg'])
                    else:
                        wechat_manager.send_text(
                            wechat_client_id, my_wxid, '1群有人发违规内容：' + res['reason'])
                elif message_data['to_wxid'] == value[2] and message_data['from_wxid'] != bot_wxid and bot_wxid not in message_data['at_user_list']:
                    res = request2.delay_censor_msg(
                        censor_url, message_data['msg'])
                    if res['is_pass']:
                        wechat_manager.send_text(wechat_client_id, value[0], (value[3] if key != 2 else value[3].format(
                            request.cht_to_chs(userinfo.get_nickname_by_wxid(group2_info_path, message_data['from_wxid'])))) + message_data['msg'])
                    else:
                        wechat_manager.send_text(
                            wechat_client_id, my_wxid, '2群有人发违规内容：' + res['reason'])
            # 回复单聊消息
            if message_data['to_wxid'] == bot_wxid and message_data['from_wxid'] not in not_reply_list and message_data['from_wxid'] != bot_wxid:
                now = datetime.now()
                bot_res_json = request.bot_reply(
                    bot_url, bot_url2, message_data['msg'])
                now2 = datetime.now()
                print('机器人请求耗时:' + str((now2 - now).total_seconds()))
                if bot_res_json['content'] != '':
                    wechat_manager.send_text(
                        wechat_client_id, message_data['from_wxid'], bot_res_json['content'])
            # 回复群@消息
            if bot_wxid in message_data['at_user_list'] and message_data['from_wxid'] != bot_wxid and message_data['to_wxid'] not in not_reply_list:
                # 判断@在前还是在后
                if message_data['msg'][0] == '@':
                    split_at_msg = message_data['msg'].split('\u2005', 1)
                    if len(split_at_msg) == 1:
                        split_at_msg = message_data['msg'].split(' ', 1)

                    if len(split_at_msg) == 1:
                        at_msg = split_at_msg[0]
                    else:
                        at_msg = split_at_msg[1]
                else:
                    at_msg = message_data['msg'].split('@', 1)[0]
                print(at_msg)
                bot_res_json = dict()
                if at_msg:
                    bot_res_json = request.bot_reply(bot_url, bot_url2, at_msg)
                else:
                    bot_res_json['content'] = '艾特我的时候要说点儿什么。。'
                print(bot_res_json)
                at_reply_list = [message_data['from_wxid']]
                wechat_manager.send_chatroom_at_msg(
                    wechat_client_id, message_data['room_wxid'], '{$@}' + bot_res_json['content'], at_reply_list)

            # 不是@消息，但是可以提供答案，然后回复消息
            bot_reply_type(wechat_client_id, message_data)

        while not msg_picture_queue.empty():
            message_data = msg_picture_queue.get()
            for value in exchange_msg_room_wxid.values():
                # print(value)
                if message_data['to_wxid'] == value[0] and message_data['from_wxid'] != bot_wxid:
                    if ocr_switch == False:
                        wechat_manager.send_image(
                            wechat_client_id, value[2], message_data['image'])
                    else:
                        img = dat2img_main(message_data['image'])
                        text = get_ocr_text(ocr_main(ocr_url, img))
                        res = request2.delay_censor_msg(censor_url, text)
                        is_pass = res['is_pass']
                        if is_pass:
                            wechat_manager.send_image(
                                wechat_client_id, value[2], message_data['image'])
                        else:
                            wechat_manager.send_text(
                                wechat_client_id, my_wxid, '1群有人发违规图片：' + res['reason'])
                elif message_data['to_wxid'] == value[2] and message_data['from_wxid'] != bot_wxid:
                    if ocr_switch == False:
                        wechat_manager.send_image(
                            wechat_client_id, value[0], message_data['image'])
                    else:
                        img = dat2img_main(message_data['image'])
                        text = get_ocr_text(ocr_main(ocr_url, img))
                        res = request2.delay_censor_msg(censor_url, text)
                        is_pass = res['is_pass']
                        if is_pass:
                            wechat_manager.send_image(
                                wechat_client_id, value[0], message_data['image'])
                        else:
                            wechat_manager.send_text(
                                wechat_client_id, my_wxid, '2群有人发违规图片：' + res['reason'])

        while not msg_voice_queue.empty():
            message_data = msg_voice_queue.get()
            for value in exchange_msg_room_wxid.values():
                if message_data['to_wxid'] == value[0] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_file(
                        wechat_client_id, value[2], message_data['silk_file'])
                elif message_data['to_wxid'] == value[2] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_file(
                        wechat_client_id, value[0], message_data['silk_file'])

        while not msg_video_queue.empty():
            message_data = msg_video_queue.get()
            for value in exchange_msg_room_wxid.values():
                if message_data['to_wxid'] == value[0] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_video(
                        wechat_client_id, value[2], message_data['video'])
                elif message_data['to_wxid'] == value[2] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_video(
                        wechat_client_id, value[0], message_data['video'])

        while not msg_file_queue.empty():
            message_data = msg_file_queue.get()
            for value in exchange_msg_room_wxid.values():
                if message_data['to_wxid'] == value[0] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_file(
                        wechat_client_id, value[2], message_data['file'])
                elif message_data['to_wxid'] == value[2] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_file(
                        wechat_client_id, value[0], message_data['file'])

        while not msg_emoji_queue.empty():
            message_data = msg_emoji_queue.get()
            for value in exchange_msg_room_wxid.values():
                if message_data['to_wxid'] == value[0] and message_data['from_wxid'] != bot_wxid:
                    file_path = gif_is_can_send(message_data['raw_msg'])
                    if file_path != '':
                        wechat_manager.send_gif(
                            wechat_client_id, value[2], file_path)
                elif message_data['to_wxid'] == value[2] and message_data['from_wxid'] != bot_wxid:
                    file_path = gif_is_can_send(message_data['raw_msg'])
                    if file_path != '':
                        wechat_manager.send_gif(
                            wechat_client_id, value[0], file_path)

        while not msg_link_queue.empty():
            message_data = msg_link_queue.get()
            for value in exchange_msg_room_wxid.values():
                link_info = rawmsg.get_link_msg_info(message_data['raw_msg'])
                title = link_info['title'] if link_info['title'] != None else ''
                desc = link_info['des'] if link_info['des'] != None else ''
                url = link_info['url'] if link_info['url'] != None else ''
                if url == '':
                    break
                url = url.replace('&', '&amp;')
                image_url = link_info['thumburl'] if link_info['thumburl'] != None else ''
                image_url = image_url.replace('&', '&amp;')
                default_image_url = return_link_thumb_url().replace('&', '&amp;')
                image_url = default_image_url if image_url.strip() == '' else image_url
                if message_data['to_wxid'] == value[0] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_link(
                        wechat_client_id, value[2], title, desc, url, image_url)
                elif message_data['to_wxid'] == value[2] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_link(
                        wechat_client_id, value[0], title, desc, url, image_url)

        while not msg_miniapp_queue.empty():
            message_data = msg_miniapp_queue.get()
            for key, value in exchange_msg_room_wxid.items():
                if message_data['to_wxid'] in value:
                    wechat_manager.send_text(
                        wechat_client_id, my_wxid, '有人在群里发送了小程序！')

        while not msg_other_app_queue.empty():
            message_data = msg_other_app_queue.get()
            for value in exchange_msg_room_wxid.values():
                link_info = rawmsg.get_link_msg_info(message_data['raw_msg'])
                title = link_info['title'] if link_info['title'] != None else ''
                desc = link_info['des'] if link_info['des'] != None else ''
                url = link_info['url'] if link_info['url'] != None else ''
                if url == '':
                    break
                url = url.replace('&', '&amp;')
                image_url = link_info['thumburl'] if link_info['thumburl'] != None else ''
                image_url = image_url.replace('&', '&amp;')
                default_image_url = return_link_thumb_url().replace('&', '&amp;')
                image_url = default_image_url if image_url.strip() == '' else image_url
                if message_data['to_wxid'] == value[0] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_link(
                        wechat_client_id, value[2], title, desc, url, image_url)
                elif message_data['to_wxid'] == value[2] and message_data['from_wxid'] != bot_wxid:
                    wechat_manager.send_link(
                        wechat_client_id, value[0], title, desc, url, image_url)
