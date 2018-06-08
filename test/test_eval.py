#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 18:09
# @Author  : jiakang
# @File    : test_eval.py
# @Software: IntelliJ IDEA


def my_print(*args):
    print(args)


def do_foo():
    print('foo')


def do_bar():
    print('bar')


# eval('my_print', None, {'hehe': 'haha'})
# eval('do_foo')()
# eval('my_print')('haha', 'hehe')
f = eval('test_none')
f('haha')
