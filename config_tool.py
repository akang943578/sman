#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/14 17:54
# @Author  : jiakang
# @File    : config_tool.py
# @Software: IntelliJ IDEA

import os
import os.path as path
import ConfigParser
import install, utils

sman_cfg_path = install.sman_cfg_path


def __usage(prompt=None, extra_usage=None):
    if prompt:
        utils.print_err(prompt)
    if extra_usage:
        utils.print_normal(extra_usage)
    exit(0)


def check_config(create=False):
    if path.exists(sman_cfg_path) and path.isfile(sman_cfg_path):
        return
    if create:
        os.system('touch %s' % sman_cfg_path)
        return
    __usage('没有找到配置文件：%s' % sman_cfg_path)


def get_option(section, option, default, tip_str=None, check_exist=False):
    cf = ConfigParser.ConfigParser()
    cf.read(sman_cfg_path)

    if check_exist:
        check_config()
        if not cf.has_section(section):
            __usage('配置文件：%s 配置域缺失：%s' % (sman_cfg_path, section), tip_str)

    if cf.has_option(section, option):
        return cf.get(section, option)
    if default is not None:
        return default
    __usage('配置文件：%s 配置域：%s 配置项缺失：%s' % (sman_cfg_path, section, option), tip_str)


def set_option(section, option, value):
    check_config(True)
    cf = ConfigParser.ConfigParser()
    cf.read(sman_cfg_path)

    if not cf.has_section(section):
        cf.add_section(section)

    cf.set(section, option, value)
    cf.write(open(sman_cfg_path, 'w'))
