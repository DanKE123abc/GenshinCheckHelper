import setting

#--------MD5计算------------
import hashlib

def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()
#---------------------------

#--------随机文本------------
import random
import string

def random_text(num: int) -> str:
    return ''.join(random.sample(string.ascii_lowercase + string.digits, num))
#---------------------------

#--------时间戳-------------
import time

def timestamp() -> int:
    return int(time.time())
#---------------------------

#----------获取ds-----------
def getDS():
    n = setting.bbs_Salt
    i = str(timestamp())
    r = random_text(6)
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return "{},{},{}".format(i, r, c)
#---------------------------

#-------生成deviceID--------
import uuid

def get_device_id(cookie) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_URL, cookie))
#---------------------------

