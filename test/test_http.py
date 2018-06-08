#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/17 10:03
# @Author  : jiakang
# @File    : test_http.py
# @Software: IntelliJ IDEA

import urllib2

response = urllib2.urlopen('https://raw.githubusercontent.com/haojiakang/sman/master/sman_common.py')
common_scripts = []
for line in response.readlines():
    if line.startswith('def'):
        end = line.index('(')
        method_name = line[3:end].strip()
        if method_name != 'try_do_common':
            common_scripts.append(method_name)
            # print(method_name)