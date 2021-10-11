#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/05/16 上午11:13
# @Author  : su
# @File    : main.py
# @Software: PyCharm

import requests,os,time,json
import hmac
import hashlib
import base64
import urllib.parse
# from PIL import Image
# import matplotlib.pyplot as plt



class Tieba():

    def __init__(self, bduss,ding_secret,ding_webhook):
        self.bduss = bduss
        self.ding_secret = ding_secret
        self.ding_webhook = ding_webhook
        self.tbs_url = 'http://tieba.baidu.com/dc/common/tbs'
        self.fid_url = 'http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname='
        self.like_url = 'http://c.tieba.baidu.com/c/f/forum/like'


    def decrypt(self, data):
        SIGN_KEY = 'tiebaclient!!!'
        s = ''
        keys = data.keys()
        for i in sorted(keys):
            s += i + '=' + str(data[i])
        sign = hashlib.md5((s + SIGN_KEY).encode('utf-8')).hexdigest().upper()
        data.update({'sign': str(sign)})
        return data

    def get_tbs(self):
        headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            'Cookie': 'BDUSS=' + self.bduss,
        }
        return requests.get(url=self.tbs_url, headers=headers).json().get('tbs')

    def get_fid(self, name):
        url = self.fid_url + str(name)
        fid = requests.get(url, timeout=2).json()['data']['fid']
        return fid

    def follow(self):
        baGroup = []
        page,has_more = 1,'1'
        while has_more == '1':
            data = {
                'BDUSS': self.bduss,
                '_client_type': '2',
                '_client_id': 'wappc_1534235498291_488',
                '_client_version': '9.7.8.0',
                '_phone_imei': '000000000000000',
                'from': '1008621y',
                'page_no': str(page),
                'page_size': '200',
                'model': 'MI+5',
                'net_type': '1',
                'timestamp': str(int(time.time())),
                'vcode_tag': '11',
            }
            data = self.decrypt(data)
            try:
                res = requests.post(url=self.like_url, data=data, timeout=2).json()
                has_more = res['has_more']
                page += 1
                if 'forum_list' not in res:
                    return {"code":403,"message":'未找到关注贴吧'}
                else:
                    baGroup.append(res['forum_list'].get('non-gconforum'))
                    baGroup.append(res['forum_list'].get('gconforum'))
            except Exception as e:
                return {"code":403,"message":e}
        return {"code":200,"data":baGroup}

    def sign_one(self, name):
        tbs = self.get_tbs()
        fid = self.get_fid(name)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'ka=open',
            'User-Agent': 'bdtb for Android 9.7.8.0',
            'Connection': 'close',
            'Accept-Encoding': 'gzip',
            'Host': 'c.tieba.baidu.com',
        }
        data = {
            "BDUSS": self.bduss,
            '_client_type': '2',
            '_client_version': '9.7.8.0',
            '_phone_imei': '000000000000000',
            "fid": fid,
            'kw': name,
            'model': 'MI+5',
            "net_type": "1",
            'tbs': tbs,
            'timestamp': str(int(time.time())),
        }
        data = self.decrypt(data)
        url = 'http://c.tieba.baidu.com/c/c/forum/sign'
        try:
            res = requests.post(url=url, data=data, headers=headers).json()
            if str(res['error_code']) == '0' or str(res['error_code']) == '160002':
                return '%s签到成功' % name
            elif str(res['error_code']) == '340011':
                return '签到频繁'
            else:
                return '%s签到失败' % name
        except Exception as e:
            return(e)

    def send_message(self,message):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.ding_secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.ding_secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        request_url = f"{self.ding_webhook}&timestamp={timestamp}&sign={sign}"
        headers = {'content-type': 'application/json'}
        String_textMsg = {"msgtype": "text",
                          "text": {
                                "content": message
                            }
                          }
        requests.post(request_url, headers=headers, data=json.dumps(String_textMsg))

    def main(self):
        followInfo = self.follow().get('data')
        ba = [ba.get("name") for baGroup in followInfo for ba in baGroup]
        result = map(self.sign_one, ba)
        messageGroup = list(result)
        message = '\n'.join(messageGroup)
        tieba.send_message('百度贴吧日常签到: \n --------\n ' + message)


def get_bduss():
    s = requests.session()
    url1 = 'https://passport.baidu.com/v2/api/getqrcode?lp=pc&apiver=v3&tpl=netdisk'
    headers1 = {
        'Connection': 'keep-alive',
        'Host': 'passport.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    res1 = s.get(url=url1, headers=headers1).json()
    sign = res1['sign']
    imgurl = 'https://' + res1['imgurl']
    with open('qcode.png', 'wb') as f:
        f.write(s.get(imgurl).content)
    img = Image.open('qcode.png')
    img.show()
    time.sleep(15)

    url2 = 'https://passport.baidu.com/channel/unicast?channel_id={}&callback=&tpl=netdisk&apiver=v3'.format(sign)
    headers2 = {
        'Host': 'passport.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    res2 = s.get(url=url2, headers=headers2).text[1:-2]
    try:
        data = json.loads(res2)
        data = json.loads(data['channel_v'])
        v = data['v']
        url3 = 'https://passport.baidu.com/v3/login/main/qrbdusslogin?bduss={}&u=https%253A%252F%252Fpan.baidu.com%252Fdisk%252Fhome&loginVersion=v4&qrcode=1&tpl=netdisk&apiver=v3&traceid=&callback=%27'.format(
            v)
        response = s.get(url3)
        bduss = response.cookies['BDUSS']
        with open('cookie.txt', encoding='utf-8', mode='w+') as f:
            f.write(bduss)
    except:
        bduss = ''
        print('二维码扫描超时')
    if bduss is None:
        bduss = ''
    return bduss


if __name__ == '__main__':
    bduss = os.environ.get('BDUSS')
    ding_secret = os.environ.get('DINGTALK_SECRET')
    ding_webhook = os.environ.get('DINGTALK_WEBHOOK')
    tieba = Tieba(bduss,ding_secret,ding_webhook)
    tieba.main()
