# -*- coding: utf-8 -*-
import json
import requests
import time
import hashlib
import string
import random
import sys
from AccessToken import AccessToken

#时间：2022/9/16
#作者：蛋壳
#备注：米游社原神签到

def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()

def getDS():
    n = '1OUn34iIy84ypu9cpXyun2VaQ2zuFeLm'
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return "{},{},{}".format(i, r, c)

#微信推送
def dankepush(openid,message):
    access_token = AccessToken().get_access_token()
    body = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
        params={
            'access_token': access_token
        },
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )
    result = response.json()
    print(result)

        

class Sign:
    app_version = "2.33.1"
    act_id = "e202009291139501"
    region = "cn_gf01"
    device_id = "7ab3bc70b846186b9da1e816e6c6f08d"

    def __init__(self, uid, cookie):
        self.uid = uid
        self.cookie = cookie
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.3.0"
        }

    #请求头
    def buildHearders(self):
        self.headers["Cookie"] = self.cookie
        self.headers["x-rpc-device_id"] = Sign.device_id
        self.headers["Host"] = "api-takumi.mihoyo.com"
        self.headers["Content-type"] = "application/json;charset=utf-8"
        self.headers["Accept"] = "application/json, text/plain, */*"
        self.headers["x-rpc-client_type"] = "4"
        self.headers["x-rpc-app_version"] = Sign.app_version
        self.headers["DS"] = getDS()

    #签到原神
    def sign(self):
        signUrl = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign"
        param = {"act_id": Sign.act_id, "region": Sign.region, "uid": self.uid}
        result = requests.request("POST", signUrl, headers=self.headers, data=json.dumps(param))
        return json.loads(result.content)

    #签到信息
    def getSignInfo(self):
        url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id={}"
        userInfoResult = requests.get(url.format(Sign.act_id), headers=self.headers)
        return json.loads(userInfoResult.content)

    #签到天数
    def getTotalSignDay(self):
        url = "https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?region={}&act_id={}&uid={}"
        userInfoResult = requests.get(url.format(Sign.region, Sign.act_id, self.uid), headers=self.headers)
        return json.loads(userInfoResult.content)

    #游戏信息
    def getGameInfo(self):
        url = "https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz=hk4e_cn"
        userInfoResult = requests.get(url, headers=self.headers)
        return json.loads(userInfoResult.content)

    def main_handler(self):
        self.buildHearders()
        #签到
        signResult = self.sign()
        #游戏信息
        totalSignDay = self.getTotalSignDay()["data"]
        totalSignDay = totalSignDay["total_sign_day"]
        gameInfo = self.getGameInfo()["data"]["list"][0]
        signInfo = self.getSignInfo()["data"]
        award = signInfo["awards"][totalSignDay - 1]
        message = '''⏰当前时间：{} 
哈喽！您的米游社原神签到已经帮您完成了！
####################
😎游戏昵称：{}
🤺冒险等级：{}
💻签到结果：{}
🎁签到奖励：{} x {}
📅{}月累计签到：**{}** 天
####################
祝您过上美好的一天！
                        ——by DanKe'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800)),
                               gameInfo["nickname"],
                               gameInfo["level"],
                               signResult['message'], award['name'], award['cnt'], signInfo["month"],
                               totalSignDay)
        return message





def handler(event, context):#这里是阿里云的入口，腾讯云要改成main_handler
    config_path = "config.json"
    with open(config_path, "r") as f:
        row_data = json.load(f)

    for user in row_data:
        uid = user['UID']
        cookie = user['cookie']
        pushid = user['pushid']
        try:
            miHoYoUser = Sign(uid, cookie)
            msg = miHoYoUser.main_handler()
        except:
            msg = '签到失败，cookie可能已过期'
        #print(msg)
        dankepush(pushid, msg)

if __name__ == '__main__':
    config_path = "config.json"
    with open(config_path, "r") as f:
        row_data = json.load(f)

    for user in row_data:
        uid = user['UID']
        cookie = user['cookie']
        pushid = user['pushid']
        try:
            miHoYoUser = Sign(uid, cookie)
            msg = miHoYoUser.main_handler()
        except:
            msg = '签到失败，cookie可能已过期'
        #print(msg)
        dankepush(pushid, msg)
        

