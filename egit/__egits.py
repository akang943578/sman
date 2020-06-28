#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 15:29
# @Author  : jiakang
# @File    : __egits.py
# @Software: IntelliJ IDEA

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))
import commands, utils


# 获取用户输入的commit信息
def get_commit_msg(args=None):
    if args:
        commit_msg = ' '.join(args)
    else:
        commit_msg = raw_input('Please input commit msg: ')
    return commit_msg


# 获取当前的branch分支
def get_current_branch_name():
    current_branch_name = commands.getoutput('git symbolic-ref --short -q HEAD')
    return current_branch_name


# 判断当前分支是否有未提交的代码
def has_uncommitted_codes():
    status_result = commands.getoutput('git status')
    if ('Changes not staged for commit:' in status_result) \
            or ('Changes to be committed:' in status_result) \
            or ('尚未暂存以备提交的变更：' in status_result) \
            or ('要提交的变更：' in status_result):
        return True
    return False


# 如果在master，则退出程序
def exit_at_master(option):
    current_branch_name = get_current_branch_name()
    if current_branch_name == 'master':
        utils.print_err('The option \'%s\' not support branch master!' % option)
        exit(0)
