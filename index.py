# -*- coding: utf-8 -*-
import DKtools
import setting
import random
import captcha
import time
import json
import requests
from request import http
from wechatpush import AccessToken
#时间：2022/9/16
#作者：蛋壳
#备注：米游社原神签到




#---------------------------微信推送------------------------------------
def wechatpush(openid,message):
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
#------------------------------------------------------------------------
        

class Sign:
    app_version = "2.38.1"
    act_id = "e202009291139501"
    region = "hk4e_cn"

    def __init__(self, uid, cookie):
        self.uid = uid
        self.cookie = cookie
    
    #请求头
    def buildHearders(self, cookie):
        self.headers = {}
        self.headers.update(setting.headers)
        self.headers["DS"] = DKtools.getDS()
        self.headers['Referer'] = 'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true' \
                                  f'&act_id={setting.genshin_Act_id}&utm_source=bbs&utm_medium=mys&utm_campaign=icon'
        self.headers['Cookie'] = cookie
        self.headers['x-rpc-device_id'] = DKtools.get_device_id(cookie)

    #签到原神
    def sign(self, uid):
        header = {}
        header.update(self.headers)
        for i in range(4):
            if i != 0:
                print(f'触发验证码，即将进行第{i}次重试，最多3次')
            req = http.post(url=setting.genshin_Signurl, headers=header, json={'act_id': setting.genshin_Act_id, 'region': "hk4e_cn", 'uid': uid})
            if req.status_code == 429:
                time.sleep(10)  # 429同ip请求次数过多，尝试sleep10s进行解决
                print(f'429 Too Many Requests ，即将进入下一次请求')
                continue
            data = req.json()
            if data["retcode"] == 0 and data["data"]["success"] == 1:
                validate = captcha.game_captcha(data["data"]["gt"], data["data"]["challenge"])
                if validate is not None:
                    header["x-rpc-challenge"] = data["data"]["challenge"]
                    header["x-rpc-validate"] = validate
                    header["x-rpc-seccode"] = f'{validate}|jordan'
                time.sleep(random.randint(6, 15))
            else:
                break
        return json.loads(req.content)

    #签到信息
    def getSignInfo(self, region: str, uid: str) -> dict:
        req = http.get(setting.genshin_Is_signurl.format(setting.genshin_Act_id, region, uid), headers=self.headers)
        data = req.json()
        if data["retcode"] != 0:
            print("账号签到信息获取失败: "+req.text)
        return data["data"]

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
        self.buildHearders(cookie)
        #签到
        signResult = self.sign(uid)
        #游戏信息
        totalSignDay = self.getTotalSignDay()["data"]
        totalSignDay = totalSignDay["total_sign_day"]
        gameInfo = self.getGameInfo()["data"]["list"][0]
        signInfo = self.getSignInfo()
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
            msg = miHoYoUser.main_handler(cookie,uid)
        except:
            msg = '签到失败，cookie可能已过期'
        #print(msg)
        wechatpush(pushid, msg)

if __name__ == '__main__':
    config_path = "config.json"
    with open(config_path, "r") as f:
        row_data = json.load(f)

    for user in row_data:
        uid = user['UID']
        cookie = user['cookie']
        pushid = user['pushid']
        miHoYoUser = Sign(uid, cookie)
        msg = miHoYoUser.main_handler()
        #print(msg)
        wechatpush(pushid, msg)
        

