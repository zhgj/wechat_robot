#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : NextReply.py
# @Author: Administrator
# @Date  : 2020/1/2
import random


def reply_ok(until, first_msg, sb):
    return random.choice((
        "好的，我将会在%s%s提醒%s%s" % (until, first_msg, "你" if sb else "ta", reply_ok_emojins()),
        "👌 %s%s我会提醒%s%s" % (until, first_msg, "你" if sb else "ta", reply_ok_emojins()),
        "记下了，我将会在%s%s提醒%s%s" % (until, first_msg, "你" if sb else "ta", reply_ok_emojins())
    ))


def reply_ok_emojins():
    return random.choice(('😉', '😙', '🙃', '☺'))


def return_link_thumb_url():
    return random.choice(('https://github.githubassets.com/images/modules/site/home/globe.jpg', 
    'https://www.showdoc.com.cn/server/api/attachment/visitfile/sign/0203e82433363e5ff9c6aa88aa9f1bbe?showdoc=.jpg)', 
    'https://wx2.sinaimg.cn/orj360/005WA1rRgy1gs991rv3laj30u00u00u0.jpg', 
    'http://pics2.baidu.com/feed/21a4462309f79052b528fd43d8b57acc7bcbd561.png?token=bd52821ab6ba0d497a4f5503ce9b8856', 
    'https://files.catbox.moe/k7vdg4.png', 
    'https://files.catbox.moe/18gpyg.png'))
