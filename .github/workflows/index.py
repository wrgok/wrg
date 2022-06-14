# -*- coding: utf8 -*-
import re
import json
import requests
from pushplus import pushplus
from config import COOKIE, SIGN_URL, TOKEN

json_pattern = 'QZOutputJson=\((.*?)\)'


def tencent_video():
    sign_url = SIGN_URL
    sign_headers = {
        'cookie': COOKIE
    }
    res = requests.get(url=sign_url, headers=sign_headers).text
    res_json_list = re.findall(json_pattern, res)
    res_json = json.loads(res_json_list[0])
    if res_json['ret'] == 0:
        score = res_json['checkin_score']
        if score == '0':
            content = f'Cookie有效!当天已签到'
            res = pushplus(content, TOKEN)
            print(res)
        else:
            content = f'Cookie有效!签到成功,获得经验值{score}'
            res = pushplus(content, TOKEN)
            print(res)
    else:
        content = 'Cookie失效!'
        res = pushplus(content, TOKEN)
        print(res)


def main_handler(event, context):
    tencent_video()


if __name__ == '__main__':
    if SIGN_URL or COOKIE == '':
        print('请先填写config.py文件后再运行!')
    else:
        tencent_video()
