#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/8 10:30
# @Author  : jiakang
# @File    : try_write.py
# @Software: IntelliJ IDEA

import ConfigParser


def try_write():
    cf = ConfigParser.ConfigParser()
    try:
        cf.read('/Users/david/.mtool_config.bsssdfadsfafdadsfasak')
    except:
        print('.mtool_config not exist!')

    if not cf.has_section('jumper'):
        print('not has jumper')
    else:
        cf.set('jumper', 'jumper_ck', 'test-ck')
        cf.write(open('/Users/david/.mtool_config.bak', 'w'))
        print('has jumper')


if __name__ == '__main__':
    try_write()