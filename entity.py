from hoshino import Service
from hoshino.util import escape
import requests
import hashlib
import time
import base64
import hmac


secret_id = ""
secret_key = ""

sv = Service('名词描述')
def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str


def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)


@sv.on_prefix('什么是')
async def Entity(bot, ev):
    endpoint = "nlp.tencentcloudapi.com"
    data = {
        'Action': 'DescribeEntity',
        'Nonce': 11886,
        'Region': 'ap-guangzhou',
        'SecretId': secret_id,
        'Timestamp': int(time.time()),
        'Version': '2019-04-08',
    }
    data['EntityName'] = escape(ev.message.extract_plain_text().strip())
    query = data['EntityName']
    s = get_string_to_sign("GET", endpoint, data)
    data["Signature"] = sign_str(secret_key, s, hashlib.sha1)

    resp = requests.get("https://" + endpoint, params=data)
    str1 = str(resp.content, encoding="utf-8")
    data = eval(str1)
    if 'Error' in data['Response']:
        await bot.send(ev, query + ': ' + data['Response']['Error']['Message'])
        return
    str1 = str(bytes(data['Response']['Content'].encode('utf-8')), encoding="utf-8")
    data = eval(str1)
    res = ''
    if '简介' not in data:
        for i in data['精选上位词']:
            res += i['Name'] + ', '
        await bot.send(ev, query + ': ' + res)
        return
    msg = data['简介'][0]['Name']
    if len(msg) > 100:
        if type(len(msg) / 2) == int:
            num = 1
        else:
            num = 0
        await bot.send(ev, query + ': ' + msg[0:int(len(msg) / 2)])
        await bot.send(ev, msg[int(len(msg) / 2) + num:])
        return
    await bot.send(ev, query + ': ' + data['简介'][0]['Name'])
