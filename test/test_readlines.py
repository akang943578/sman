#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 19:36
# @Author  : jiakang
# @File    : test_readlines.py
# @Software: IntelliJ IDEA


with open('/usr/local/bin/sman', 'r') as f:
    for line in f.readlines():
        if line.startswith('sman_path'):
            install_path = line[14:-2]
            print(install_path)
