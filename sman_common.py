#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 17:55
# @Author  : jiakang
# @File    : sman_common.py
# @Software: IntelliJ IDEA

import os
import os.path as path
import install
import shutil
import config_tool, utils
import commands

sman_section = 'sman'
git_repo_prefix = 'git@github.com:'
sman_work_dir = os.getcwd()
install_dir = install.get_install_dir()


def try_do_common(script, args):
    try:
        f = eval(script)
    except NameError as e:
        return False

    f(args)
    return True


def list(args):
    sman_dir = install.get_install_dir()
    if len(args) > 0:
        utils.print_err('too many args')
        return

    base_scripts_dirs = install.get_base_scripts_dirs(sman_dir)
    for fetch_dir in base_scripts_dirs:
        abs_fetch_dir = path.join(sman_dir, fetch_dir)
        __find_script_display(fetch_dir, abs_fetch_dir)

    custom_scripts_dirs = install.get_custom_dirs(sman_dir)
    for custom_scripts_dir in custom_scripts_dirs:
        abs_fetch_dir = install.get_custom_scripts_dir(custom_scripts_dir)
        __find_script_display(path.basename(custom_scripts_dir), abs_fetch_dir)


def __find_script_display(module_name, dir_path):
    utils.print_tip('============== %s ==============' % module_name)
    listfiles = os.listdir(dir_path)
    for filename in listfiles:
        script_path = path.join(dir_path, filename)
        if install.should_script_gather_with_sman(script_path, filename):
            script_discript = filename + ' : '
            with open(script_path) as f:
                for line in f.readlines():
                    for notes_str in ['# sman_notes:', '#sman_notes:']:
                        if line.startswith(notes_str):
                            start_pot = len(notes_str)
                            script_discript += line[start_pot:].strip()
                            break
            print(script_discript)
    print('')


def update(args=None):
    if args and len(args) > 0:
        utils.print_err('too many args')
        return

    utils.print_tip('updating sman...')
    os.system('git -C "%s" pull' % install_dir)

    custom_scripts_dirs = install.get_custom_dirs(install_dir)
    for custom_scripts_dir in custom_scripts_dirs:
        utils.print_tip('updating custom module folder \'%s\'...' % path.basename(custom_scripts_dir))
        os.system('git -C "%s" pull' % custom_scripts_dir)

    install.walk_and_gen_tab_complete(install_dir, True)
    __set_last_updated_day()


def __set_last_updated_day():
    config_tool.set_option(sman_section, install.sman_last_update_day_key, install.get_current_day())


def add(args):
    if len(args) != 1:
        utils.print_err('args len is not 1, please input like name/module')
        return

    module = args[0]
    module_split = str.split(module, '/')
    if len(module_split) <= 1:
        return

    module_name = module.replace('/', '_')
    module_dir = path.join(install_dir, 'custom', module_name)

    if path.exists(module_dir) and path.isdir(module_dir):
        if __read_input('module \'%s\' is already exists, re add it?' % module):
            shutil.rmtree(module_dir)
        else:
            return
    os.system('git clone %s%s.git --depth=1 "%s"' % (git_repo_prefix, module, module_dir))

    install.walk_and_gen_tab_complete(install_dir, True)
    print('module \'%s\' added completed.' % module)


def rm(args):
    if len(args) != 1:
        utils.print_err('args len is not 1, please input like name/module')
        return

    module = args[0]
    if __read_input('you input is %s, really want to rm this module?' % module):
        module_name = module.replace('/', '_')
        module_dir = path.join(install_dir, 'custom', module_name)

        if path.exists(module_dir) and path.isdir(module_dir):
            shutil.rmtree(module_dir)
            install.walk_and_gen_tab_complete(install_dir, True)
            print('module \'%s\' removed completed.' % module)
        else:
            print('module \'%s\' not exists!' % module)


def uninstall(args):
    if len(args) > 0:
        utils.print_err('too many args')
        return

    if __read_input('really want to remove sman?'):
        install.check_exists(True)


def reinstall(args):
    if len(args) > 0:
        utils.print_err('too many args')
        return

    install.install()


def __read_input(prompt):
    input_strs = ['y', 'n']
    while True:
        input = raw_input(prompt + ' [y/n]: ')
        lower_input = str.lower(input.strip())
        if lower_input not in input_strs:
            continue
        return lower_input == 'y'


def __check_auto_update():
    sman_auto_check_update = __get_bool_from_sman_section(install.sman_auto_check_update_key,
                                                            install.sman_auto_check_update_value)
    sman_promt_update_verify = __get_bool_from_sman_section(install.sman_prompt_update_verify_key,
                                                              install.sman_prompt_update_verify_value)
    sman_update_days_gap = __get_int_from_sman_section(install.sman_update_days_gap_key,
                                                         install.sman_update_days_gap_value)
    sman_last_update_day = __get_int_from_sman_section(install.sman_last_update_day_key,
                                                     install.sman_last_update_day_value)
    beyond_update_gap = install.get_current_day() - sman_last_update_day >= sman_update_days_gap

    if sman_auto_check_update:
        if __need_update_multi(beyond_update_gap):
            if sman_promt_update_verify:
                prompt = '[sman] Would you like to update?'
                if __read_input(prompt):
                    update()
                else:
                    __set_last_updated_day()
            else:
                update()


def __need_update_multi(beyond_update_gap):
    install_dir_update = __need_update(install_dir, beyond_update_gap)
    if install_dir_update:
        return True

    custom_scripts_dirs = install.get_custom_dirs(install_dir)
    for custom_scripts_dir in custom_scripts_dirs:
        custom_dir_update = __need_update(custom_scripts_dir, beyond_update_gap)
        if custom_dir_update:
            return True
    return False


def __need_update(git_dir, beyond_update_gap):
    # print('checking for update...')
    fetch_result = commands.getoutput('git -C "%s" fetch' % git_dir)
    if fetch_result or beyond_update_gap:
        gst_result = commands.getoutput('git -C "%s" status' % git_dir)
        if 'use "git pull" to update' in gst_result:
            return True
    return False


def __get_bool_from_sman_section(key, default):
    value = config_tool.get_option(sman_section, key, default)
    return str.lower(value) == 'true'


def __get_int_from_sman_section(key, default):
    value = config_tool.get_option(sman_section, key, default)
    return int(value)
