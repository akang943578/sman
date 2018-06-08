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

git_repo_prefix = 'git@github.com:'
sman_work_dir = os.getcwd()


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
        print('too many args')
        return

    base_scripts_dirs = install.get_base_scripts_dirs(sman_dir)
    for fetch_dir in base_scripts_dirs:
        abs_fetch_dir = path.join(sman_dir, fetch_dir)
        __find_script_display(fetch_dir, abs_fetch_dir)

    custom_scripts_dirs = install.get_custom_scripts_dirs(sman_dir)
    for custom_scripts_dir in custom_scripts_dirs:
        abs_fetch_dir = path.join(sman_dir, 'custom', custom_scripts_dir, 'scripts')
        __find_script_display(custom_scripts_dir, abs_fetch_dir)


def __find_script_display(module_name, dir_path):
    print('============== %s ==============' % module_name)
    listfiles = os.listdir(dir_path)
    for filename in listfiles:
        script_path = path.join(dir_path, filename)
        if path.isfile(script_path) and filename != '__init__.py' and not filename.startswith('_'):
            script_discript = filename + ' : '
            with open(script_path) as f:
                notes_str = '# sman_notes:'
                for line in f.readlines():
                    if line.startswith(notes_str):
                        start_pot = len(notes_str)
                        script_discript += line[start_pot:].strip()
                        break
            print(script_discript)
    print('')


def update(args):
    # print('update')
    if len(args) > 0:
        print('too many args')
        return

    install_dir = install.get_install_dir()
    print('update sman...')
    os.system('git -C "%s" pull' % install_dir)

    custom_scripts_dirs = install.get_custom_scripts_dirs(install_dir)
    for custom_scripts_dir in custom_scripts_dirs:
        print('update custom module folder \'%s\'' % custom_scripts_dir)
        os.system('git -C "%s" pull' % path.join(install_dir, 'custom', custom_scripts_dir))

    install.walk_and_gen_tab_complete(install_dir, True)


def add(args):
    # print('add')
    if len(args) != 1:
        print('args len is not 1, please input like name/module')
        return

    module = args[0]
    module_split = str.split(module, '/')
    if len(module_split) <= 1:
        return

    install_dir = install.get_install_dir()
    module_name = module.replace('/', '_')
    module_dir = path.join(install_dir, 'custom', module_name)
    # print(module_dir)

    if path.exists(module_dir) and path.isdir(module_dir):
        if __read_input('module \'%s\' is already exists, re add it?' % module):
            shutil.rmtree(module_dir)
        else:
            return
    os.system('git clone %s%s.git --depth=1 "%s"' % (git_repo_prefix, module, module_dir))

    install.walk_and_gen_tab_complete(install_dir, True)
    print('module \'%s\' added completed.' % module)


def rm(args):
    # print('
    if len(args) != 1:
        print('args len is not 1, please input like name/module')
        return

    module = args[0]
    if __read_input('you input is %s, really want to rm this module?' % module):
        install_dir = install.get_install_dir()
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
        print('too many args')
        return

    if __read_input('really want to remove sman?'):
        install.check_exists(True)


def reinstall(args):
    if len(args) > 0:
        print('too many args')
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
