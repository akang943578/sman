#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 19:24
# @Author  : jiakang
# @File    : __config_tool.py
# @Software: IntelliJ IDEA
import ConfigParser
import os.path as path
import os

mtool_cfg_path = os.environ['HOME'] + '/.mtool_config'
jumper_section = 'jumper'


def __usage(prompt=None):
    if prompt:
        print(prompt)
    tip_str = '''请在$HOME根目录下创建.mtool_config文件，并配置需要的值。示例：
    
[jumper]
jumper_user=haojiakang
jumper_passwd=******
jumper_ip=jumper.sankuai.com

jumper_u=1431393780
jumper_dt=2
jumper_ai=1
jumper_ck=411b78ff-83d4-406b-b6f6-f6b335bff537


注意：
jumper_ip可以不配置，默认是jumper.sankuai.com
    '''
    print(tip_str)
    exit(0)


def check_config():
    if path.exists(mtool_cfg_path) and path.isfile(mtool_cfg_path):
        pass
    else:
        __usage('没有找到配置文件：%s' % mtool_cfg_path)


def __get_option(cfg_path, cf, section, option, default):
    if cf.has_option(section, option):
        return cf.get(section, option)
    if default:
        return default
    __usage('配置文件：%s 配置域：%s 配置项缺失：%s' % (cfg_path, section, option))


def get_jumper_option(option_name, default_value=None):
    cf = ConfigParser.ConfigParser()

    if not path.exists(mtool_cfg_path) or not path.isfile(mtool_cfg_path):
        __usage('配置文件：%s 不存在或不是文件' % mtool_cfg_path)
    cf.read(mtool_cfg_path)

    if not cf.has_section(jumper_section):
        __usage('配置文件：%s 配置域缺失：%s' % (mtool_cfg_path, jumper_section))

    return __get_option(mtool_cfg_path, cf, jumper_section, option_name, default_value)


def set_jumper_option(option_name, value):
    cf = ConfigParser.ConfigParser()
    cf.read(mtool_cfg_path)

    if not cf.has_section(jumper_section):
        cf.add_section(jumper_section)

    cf.set(jumper_section, option_name, value)
    cf.write(open(mtool_cfg_path, 'w'))
    # print('配置文件：%s 配置域：%s 配置项：%s=%s 已设置' % (mtool_cfg_path, jumper_section, option_name, value))


if __name__ == '__main__':
    get_jumper_option()