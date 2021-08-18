from nonebot import on_command, CommandSession
from nonebot import permission as perm

from hoshino import Service
from hoshino.util  escape
from hoshino.typing import CQEvent
from datetime import datetime, timedelta
import warnings
import sys
import uuid
import requests
import hashlib
import time
from importlib import reload

import time
sv = Service('translate')
true="true"
false="flse"
reload(sys)
YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = ''
APP_SECRET = ''
data = {}

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

def sconnect(q):
    warnings.simplefilter('ignore',ResourceWarning)
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['from'] = 'auto'
    data['appKey'] = APP_KEY
    data['q']=q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = "您的用户词表ID"

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        pass
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        ssr=response.content
        str1=str(ssr, encoding = "utf-8")  
        sss=eval(str1)
        print(sss)
        if not 'basic' in sss.keys():
            return sss['translation']
            
        return sss['basic']['explains']

@sv.on_prefix('翻译英')
async def whois(bot, ev: CQEvent):
    q = escape(ev.message.extract_plain_text().strip())
    data['to'] = 'en'
    res=sconnect(q)
    await bot.send(ev,(str)(res))
    
@sv.on_prefix('翻译中')
async def whois(bot, ev: CQEvent):
    q = escape(ev.message.extract_plain_text().strip())
    data['to'] = 'zh-CHS'
    res=sconnect(q)
    await bot.send(ev,(str)(res))
    
@sv.on_prefix('翻译日')
async def whois(bot, ev: CQEvent):
    q = escape(ev.message.extract_plain_text().strip())
    data['to'] = 'ja'
    res=sconnect(q)
    await bot.send(ev,(str)(res))
    