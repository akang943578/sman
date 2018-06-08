#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 13:23
# @Author  : jiakang
# @File    : __code_tool.py
# @Software: IntelliJ IDEA

import json, urllib2, os, base64, time, commands, __config_tool, __totp, sys


def get_verification_code():
    jumper_u = __config_tool.get_jumper_option('jumper_u')
    jumper_dt = __config_tool.get_jumper_option('jumper_dt')
    jumper_ai = __config_tool.get_jumper_option('jumper_ai')

    if len(sys.argv) > 1:
        jumper_ck = sys.argv[1]
        __config_tool.set_jumper_option('jumper_ck', jumper_ck)
    else:
        jumper_ck = __config_tool.get_jumper_option('jumper_ck')

    header_dict = {
        'u': jumper_u,
        'dt': jumper_dt,
        'ai': jumper_ai,
        'ck': jumper_ck,
        'os': 'ios',
        'Content-Type': 'application/json;charset=UTF-8',
        # 'User-Agent': '%E5%A4%A7%E8%B1%A1/317 CFNetwork/758.5.3 Darwin/15.6.0'
    }
    data_dict = {
        # "ip": "192.168.1.106",
        # "ua": "ios9.3.1",
        # "timestamp": int(time.time() * 1000)
    }
    data_json = json.dumps(data_dict)

    url = 'https://api.neixin.cn/mtinfo/api/v1/tvsToken/get'
    req = urllib2.Request(url=url, data=data_json, headers=header_dict)
    res = urllib2.urlopen(req).read()

    json_data = json.loads(res)['data']
    if 'value' not in json_data:
        code = 0
    else:
        seed = json_data['value']
        code = __get_code_from_seed(seed)

    print(code)
    return code


def __get_code_from_seed(seed):
    raw_seed = base64.b64decode(seed)

    # code = commands.getoutput('oathtool --totp -b -d 6 %s' % raw_seed)
    code = __totp.get_totp(raw_seed)
    return code


if __name__ == '__main__':
    get_verification_code()
