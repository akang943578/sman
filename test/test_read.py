#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15 15:54
# @Author  : jiakang
# @File    : test_read.py
# @Software: IntelliJ IDEA
# import read_line

# read = raw_input('please input: ')

# read_line.read_input()
import os


def read_input():
    # result = raw_input('please input: ')
    # process = os.popen('read choice < /dev/tty && echo $choice')
    # system = process.read()
    # input_str = str.strip(str(system))
    # print(input_str)
    # print(input_str == 'haha')
    # print('haha' == 'haha')

    process = os.popen('read -p "please input [y/n]: " choice < /dev/tty && echo $choice')
    read = process.read()
    print(read)


read_input()

