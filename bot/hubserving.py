# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import requests
import json
import base64


def cv2_to_base64(image):
    return base64.b64encode(image).decode('utf8')


def ocr_main(url, image_file):
    try:
        img = open(image_file, 'rb').read()
        if img is None:
            print("error in loading image:{}".format(image_file))
            return ''

        headers = {"Content-type": "application/json"}
        # 发送HTTP请求
        starttime = time.time()
        data = {'images': [cv2_to_base64(img)]}
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        elapse = time.time() - starttime

        print("Predict time of %s: %.3fs" % (image_file, elapse))
        res = r.json()
        # print(res)
        return res
    except Exception as e:
        print('图像识别接口请求出现了异常：{0}'.format(e))
        return ''


def get_ocr_text(ocr_result):
    if ocr_result == '':
        return ''
    result_list = ocr_result["results"][0]
    text = ''
    for one_result in result_list:
        text += (one_result['text'] + '\n')
    text = text.strip()
    print(text)
    return text


# if __name__ == '__main__':
#     server_url = 'http://127.0.0.1:9890/predict/ocr_system'
#     image_path = r'D:\paddleocr\wuye.jpg'
#     result = ocr_main(server_url, image_path)
#     get_ocr_text(result)
