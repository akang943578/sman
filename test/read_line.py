#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15 16:02
# @Author  : jiakang
# @File    : read_line.py
# @Software: IntelliJ IDEA


# def read_input():
#     result = raw_input('please input: ')
#     print(result)
import os
import os.path as path

module = 'haojiakang/custom_scripts'
install_dir = '/Users/jiakang/sman'
os.system('git clone git@github.com:%s.git --depth=1 "%s"' % (module, path.join(install_dir, 'custom')))
