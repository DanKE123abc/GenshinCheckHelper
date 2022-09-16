# GenshinSignHelper

## 原神米游社签到助手

本程序参考genshin-check-in和genshinhelper

### 起因

因为本人是一名学生，时常忘记要签到原神，导致每个月只能签到几天（哭），一开始我用的是阿里云+genshinhelper+sever酱，但是sever酱最近收费了，每天只能用五次，我想把genshinhelper的推送改到微信测试号上，但genshinhelper因为功能太多导致改起来很麻烦，想到这里我还不如自己写一个，参考网上的资料和genshin-check-in等项目做出了此程序。


### 安装教程

##### 1.抓取cookie

​	在电脑上登录https://bbs.mihoyo.com/ys/

​	新建一个书签，内容为：

​	*javascript:(function(){let domain=document.domain;let cookie=document.cookie;prompt('Cookies: '+domain, cookie)})();*

​	点击书签即可抓取cookie

##### 2.登录微信公众平台：[微信公众平台 (qq.com)](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)

​	获得你的微信测试号，在./AccessToken.py里修改appid与appsecret即可

​	关注你的微信测试号，得到你的推送id（pushid）

##### 3.修改./config.json

​	UID填入你的原神uid

​	cookie填入你的cookie

​	pushid填入你需要推送的微信id

​	*支持多用户，自行研究*

### 待续

todo
