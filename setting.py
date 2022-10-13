bbs_Salt = "yUZ3s0Sna1IrSNfk29Vo6vRapdOyqyhB"
bbs_Version = "2.38.1"
bbs_Client_type_web = "5"  #mobile web


headers = {#请求头
    'Accept': 'application/json, text/plain, */*',
    'DS': "",
    "x-rpc-channel": "miyousheluodi",
    'Origin': 'https://webstatic.mihoyo.com',
    'x-rpc-app_version': bbs_Version,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) '
                  f'Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36 miHoYoBBS/{bbs_Version}',
    'x-rpc-client_type': bbs_Client_type_web,
    'Referer': '',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'X-Requested-With': 'com.mihoyo.hyperion',
    "Cookie": "",
    'x-rpc-device_id': ""
}

web_api = "https://api-takumi.mihoyo.com"
genshin_Act_id = "e202009291139501"
genshin_checkin_rewards = f'{web_api}/event/bbs_sign_reward/home?act_id={genshin_Act_id}'
genshin_Is_signurl = web_api + "/event/bbs_sign_reward/info?act_id={}&region={}&uid={}"
genshin_Signurl = web_api + "/event/bbs_sign_reward/sign"
