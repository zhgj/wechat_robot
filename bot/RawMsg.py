import xml.etree.ElementTree as ET

class RawMsg:
    def __format_raw_mag(self, raw_msg):
       msg = raw_msg
       return msg

    def get_link_msg_info(self, raw_msg):
        format_raw_msg = self.__format_raw_mag(raw_msg)
        root = ET.fromstring(format_raw_msg)
        link_msg = dict()
        for child in root.find('appmsg'):
            link_msg[child.tag] = child.text
        return link_msg

    def get_gif_msg_info(self, raw_msg):
        format_raw_msg = self.__format_raw_mag(raw_msg)
        root = ET.fromstring(format_raw_msg)
        return root.find('emoji').attrib


# if __name__ == '__main__':
#     xmlStr = '''<msg>\n    <fromusername>zhanggaojiong</fromusername>\n    <scene>0</scene>\n    <commenturl></commenturl>\n  
#   <appmsg appid=\"\" sdkver=\"0\">\n        <title>\u901a\u8fbe\u5b66\u5458\u6ce8\u610f\u4e86\uff0c\u6709\u4e86\u5b83\u8003\u8bd5\u5728\u4e5f\u4e0d\u7528\u7d27\u5f20\u4e86\uff01</title>\n        <des>\u901a\u8fbe\u9a7e\u6821\u79d1\u76ee\u4e09\u89c6\u9891\u8bb2\u89e3</des>\n        <action>view</action>\n        <type>5</type>\n        <showtype>0</showtype>\n        <content></content>\n        <url>http://mp.weixin.qq.com/s?__biz=MzU4NzgzNzYwOQ==&amp;mid=100007629&amp;idx=1&amp;sn=8cc7d92807b029bcad5e622e09ef41df&amp;chksm=7de4a70b4a932e1d71e12ec0725520f34a084c2ac80ced0368b0b5e53cf7786cf559d41b3f78&amp;mpshare=1&amp;scene=1&amp;srcid=04291d7zNVhKtWDyLvmiNRyy&amp;sharer_sharetime=1626101204078&amp;sharer_shareid=3e7433baee489ea8eef8a53fc6f4d8c6#rd</url>\n        <dataurl></dataurl>\n        <lowurl></lowurl>\n        <lowdataurl></lowdataurl>\n        <recorditem>\n    
#         <![CDATA[]]>\n        </recorditem>\n        <thumburl>https://mmbiz.qlogo.cn/mmbiz_jpg/oJyJzOUYZWJneBFZQFlsw2gyn1oQ9plqSSb90S2RxSNcvUoibDGPJrDGAX8Nu7fVz2S0y3IWUnFkWUF1bLbgOYQ/300?wx_fmt=jpeg&amp;wxfrom=1</thumburl>\n        <messageaction></messageaction>\n        <extinfo></extinfo>\n        <sourceusername>gh_4e6382a079ea</sourceusername>\n        <sourcedisplayname>\u9879\u57ce\u901a\u8fbe\u9a7e\u9a76\u57f9\u8bad\u5b66\u6821</sourcedisplayname>\n        <commenturl></commenturl>\n       
#  <appattach>\n            <totallen>0</totallen>\n            <attachid></attachid>\n            <emoticonmd5></emoticonmd5>\n            <fileext></fileext>\n            <cdnthumburl>3078020100046c306a0201000204b12424d802032f565d02042bc8a3b4020460ec55c5044533323262343432336461653936626637383163303565633763343534623438625f37313239666532392d323332362d343638382d383130332d3036326566626233663037350204010408030201000405004c54a100</cdnthumburl>\n            <cdnthumblength>7968</cdnthumblength>\n
#    <cdnthumbheight>150</cdnthumbheight>\n            <cdnthumbwidth>150</cdnthumbwidth>\n            <aeskey></aeskey>\n      
#       <cdnthumbaeskey>6326cfdc6b2ce117eee7b88adef9d840</cdnthumbaeskey>\n            <cdnthumblength>7968</cdnthumblength>\n  
#           <cdnthumbheight>150</cdnthumbheight>\n            <cdnthumbwidth>150</cdnthumbwidth>\n        </appattach>\n        
# <weappinfo>\n            <pagepath></pagepath>\n            <username></username>\n            <appid></appid>\n            <appservicetype>0</appservicetype>\n        </weappinfo>\n        <websearch />\n    </appmsg>\n    <appinfo>\n        <version>1</version>\n        <appname>Window wechat</appname>\n    </appinfo>\n</msg>\n'''
#     rawmsg = RawMsg()
#     info = rawmsg.get_link_msg_info(xmlStr)
#     print(info)
