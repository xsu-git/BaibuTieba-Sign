import requests
import re
import hashlib
import time
import json
from PIL import Image
#-*-conding:UTF-8 -*-

class Tieba():
    def __init__(self,bduss):
        self.bduss = bduss

    #参数解密
    def decrypt(self,data):
        SIGN_KEY = 'tiebaclient!!!'
        s = ''
        keys = data.keys()
        for i in sorted(keys):
            s += i + '=' + str(data[i])
        sign = hashlib.md5((s + SIGN_KEY).encode('utf-8')).hexdigest().upper()
        data.update({'sign': str(sign)})
        return data

    # 获取tbs
    def get_tbs(self):
        headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            'Cookie': 'BDUSS=' + self.bduss,
        }
        url = 'http://tieba.baidu.com/dc/common/tbs'
        return requests.get(url=url,headers=headers).json()['tbs']

    # 获取fid
    def get_fid(self,name):
        url = 'http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname='+str(name)
        fid = requests.get(url,timeout=2).json()['data']['fid']
        return fid

    #获取用户关注贴吧列表
    def follow(self):
        returnData = {}
        returnData['forum_list'] ={}
        i = 1
        data = {
            'BDUSS': self.bduss,
            '_client_type': '2',
            '_client_id': 'wappc_1534235498291_488',
            '_client_version': '9.7.8.0',
            '_phone_imei': '000000000000000',
            'from': '1008621y',
            'page_no': '1',
            'page_size': '200',
            'model': 'MI+5',
            'net_type': '1',
            'timestamp': str(int(time.time())),
            'vcode_tag': '11',
        }
        data = self.decrypt(data)
        url = 'http://c.tieba.baidu.com/c/f/forum/like'
        try:
            res = requests.post(url=url, data=data, timeout=2).json()
        except Exception:
            return None
        if 'forum_list' not in returnData:
            returnData['code'] = -1
            returnData['message'] = '未找到关注贴吧'
            returnData['forum_list']['non-gconforum'] = []
            returnData['forum_list']['gconforum'] = []
            return returnData

        returnData['code'] = 0
        if 'non-gconforum' in res['forum_list']:
            returnData['forum_list']['non-gconforum'] = res['forum_list']['non-gconforum']
        if 'gconforum' in res['forum_list']:
            returnData['forum_list']['gconforum'] = res['forum_list']['gconforum']
        while 'has_more' in res and res['has_more'] == '1':
            i = i + 1
            data = {
                'BDUSS': bduss,
                '_client_type': '2',
                '_client_id': 'wappc_1534235498291_488',
                '_client_version': '9.7.8.0',
                '_phone_imei': '000000000000000',
                'from': '1008621y',
                'page_no': str(i),
                'page_size': '200',
                'model': 'MI+5',
                'net_type': '1',
                'timestamp': str(int(time.time())),
                'vcode_tag': '11',
            }
            data = self.decrypt(data)
            try:
                url = 'http://c.tieba.baidu.com/c/f/forum/like'
                res = requests.post(url=url, data=data, timeout=2).json()
            except Exception:
                return None
            if 'non-gconforum' in res['forum_list']:
                returnData['forum_list']['non-gconforum'].append(res['forum_list']['non-gconforum'])
            if 'gconforum' in res['forum_list']:
                returnData['forum_list']['gconforum'].append(res['forum_list']['gconforum'])
        return returnData

    #签到
    def sign_one(self, name):
        tbs = self.get_tbs()
        fid =self.get_fid(name)
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
                print('%s签到成功'%name)
            elif str(res['error_code']) == '340011':
                 print('签到频繁')
                 time.sleep(5)
        except Exception as e:
            print(e)

    #主函数
    def main(self):
        datalist = []
        datadict = self.follow()
        if 'non-gconforum' in datadict['forum_list']:
            for m in datadict['forum_list']['non-gconforum']:
                datalist.append(m['name'])
        if 'gconforum' in datadict['forum_list']:
            for m in datadict['forum_list']['gconforum']:
                datalist.append(m['name'])
        for n in datalist:
            self.sign_one(n)

#登录
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
    with open('qcode.png','wb') as f:
        f.write(s.get(imgurl).content)
    img = Image.open('qcode.png')
    img.show()
    #等待扫码响应
    time.sleep(10)
    url2 = 'https://passport.baidu.com/channel/unicast?channel_id={}&callback=&tpl=netdisk&apiver=v3'.format(sign)
    headers2 = {
        'Host': 'passport.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    res2 = s.get(url=url2, headers=headers2).text[1:-2]
    data = json.loads(res2)
    data = json.loads(data['channel_v'])
    v = data['v']
    url3 = 'https://passport.baidu.com/v3/login/main/qrbdusslogin?bduss={}&u=https%253A%252F%252Fpan.baidu.com%252Fdisk%252Fhome&loginVersion=v4&qrcode=1&tpl=netdisk&apiver=v3&traceid=&callback=%27'.format(
        v)
    response = s.get(url3)
    bduss = response.cookies['BDUSS']
    if bduss is not None:
        return bduss
    else:
        bduss = ''
        return bduss

if __name__ == '__main__':
    bduss = get_bduss()
    if bduss:
        tieba = Tieba(bduss)
        tieba.main()
