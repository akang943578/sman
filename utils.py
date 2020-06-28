#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 15:15
# @Author  : jiakang
# @File    : utils.py
# @Software: IntelliJ IDEA

import os

BLACK = 'black'
RED = 'red'
GREEN = 'green'
YELLOW = 'yellow'
BLUE = 'blue'
PURPLE = 'purple'
CYAN = 'cyan'
WHITE = 'white'

color_code_dict = {BLACK: 30,
                   RED: 31,
                   GREEN: 32,
                   YELLOW: 33,
                   BLUE: 34,
                   PURPLE: 35,
                   CYAN: 36,
                   WHITE: 37,
                   }


# 尝试执行某命令，如果失败就退出
def try_exec(command):
    # __print_with_background_color('=======================================================')
    print_tip('Phase: %s' % command)
    code = os.system(command)
    if code != 0:
        print_err('Execute command error, so exit! Phase: %s' % command)
        exit(0)


# 用特定颜色输出内容
def print_with_front_color(msg, color=None):
    if not color:
        print(msg)
    else:
        try:
            color_code = color_code_dict[color]
            if color_code:
                print('\033[1;%dm%s\033[0m' % (color_code, msg))
        except Exception as e:
            print(msg)


# 打印错误，以红色字体
def print_err(msg):
    print_with_front_color(msg, RED)


# 打印提示，以蓝色字体
def print_tip(msg):
    print_with_front_color(msg, BLUE)


# 常规打印
def print_normal(msg):
    print_with_front_color(msg)
