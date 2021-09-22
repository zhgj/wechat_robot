from io import BufferedIOBase
import json


class UserInfo:
    def trim(seif, str):
        chars = ['-', '_', 'A', ':', '：', ' ', '的', '〈', '(', '[', ',', '，', '.', '。', '、', '~', '～', '*', '•', '·', 'de', '゛', '\ue032', '\ue022', '\ue32e', '\ue327', '\ue428' '🍃', '\ue447', '💕', '🌺', '💗']
        for char in chars:
            str = str.strip(char).replace(char, '')
        return str

    def get_nickname_by_wxid2(self, file_path, wxid):
        myfile = open(file_path, 'r')
        result = json.load(myfile)
        myfile.close()
        # print(result)
        # print(type(result))
        for member in result['member_list']:
            if member['wxid'] == wxid:
                print(member)
                if member['remark'] == '':
                    return self.trim(self.trim(member['nickname'])[0:4])
                else:
                    return self.trim(self.trim(member['remark'])[0:4]) if len(member['remark'].split('-', 1)) == 1 else self.trim(self.trim(member['remark'].split('-', 1)[1])[0:4])

    def get_nickname_by_wxid(self, file_path, wxid):
        res = self.get_nickname_by_wxid2(file_path, wxid)
        return res if res else '神秘业主'

# base_dir = r'C:\Users\zhanggaojiong\Downloads\wechat_pc_api-master\bot'
# group1_info_path = base_dir + r'\json_info\group1.json'
# group2_info_path = base_dir + r'\json_info\group2.json'

# nickname_remark = UserInfo().get_nickname_by_wxid(group1_info_path, 'zhanggaojiong')
# nickname_remark2 = UserInfo().get_nickname_by_wxid(group1_info_path, 'licaifu9855')
# nickname_remark3 = UserInfo().get_nickname_by_wxid(group2_info_path, 'wxid_rq2oy56c3epn22')
# nickname_remark4 = UserInfo().get_nickname_by_wxid(group2_info_path, 'licaifu9855')
# print(type(nickname_remark))
# print(nickname_remark)
# print(type(nickname_remark2))
# print(nickname_remark2)
# print(type(nickname_remark3))
# print(nickname_remark3)
# print(type(nickname_remark4))
# print(nickname_remark4)
