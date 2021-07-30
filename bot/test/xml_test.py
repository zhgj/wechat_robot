from os import chdir
import xml.etree.ElementTree as ET

# tree = ET.parse(r'C:\Users\zhanggaojiong\Downloads\wechat_pc_api-master\bot\link_msg2.xml')
# root = tree.getroot()
# # for child in root:
# #     print(child.tag, child.attrib)

# link_msg = dict()
# for child in root.find('appmsg'):
#     # print(child.tag, child.attrib)
#     print(child.tag, child.text)
#     link_msg[child.tag] = child.text

# print(len(link_msg))



tree = ET.parse(r'C:\Users\zhanggaojiong\Downloads\wechat_pc_api-master\bot\gif_msg.xml')
# root = tree.getroot()
# for child in root:
#     print(child.tag, child.attrib)
tree.find('emoji').attrib['cdnurl']
link_msg = dict()
for child in tree.find('emoji'):
    print(child.tag, child.attrib)
    print(child.tag, child.text)
    link_msg[child.tag] = child.text

print(len(link_msg))