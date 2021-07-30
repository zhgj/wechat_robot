# zhang = ['张红','张宏','张洪']

# msg = '谁有张宏电话？'

# flag = False
# for z in zhang:
#     print(z in msg)
#     if z in msg:
#         flag = True
#         break

# print(flag)



list = [2, 3, 4]
for i,j in range(len(list)):
    print (i,j,list[i])







reply_msg_type = {
    '收破烂电话': [['收破烂','废纸箱', '收纸箱'], 'text', ['18439451096', '18135751786', '13403851362', '15224993425','13193600443','15703890422']],
    '物业电话': [['物业','张红','张宏','张洪','张弘','张的'], 'picture', ['http://www.baidu.com', 'http://caff.ml']],
    '去周口电话': [['周口'], 'text', ['13949997920', '15516777066','13673864370','18438168828']],
    '去洛阳电话':[['洛阳'], 'text', ['44', '34']],
    '去漯河电话':[['漯河'], 'text', ['55', '67']]
}

msg = '\u8c01\u6709\u53bb\u5468\u53e3\u7684\u7535\u8bdd\uff1f'

for key, value in reply_msg_type.items():
    flag = False
    for condition in value[0]:
        if condition in msg:
            flag = True
            break
    if flag and ('电话' in msg):
        if value[1] == 'text':
            print(key + ':' + '、'.join(value[2]))
        elif value[1] == 'picture':
            for url in value[2]:
                print(key + ':' + url)
        else:
            print('其他类型消息')