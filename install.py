#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/13 09:25
# @Author  : jiakang
# @File    : install.py
# @Software: IntelliJ IDEA

import os
import os.path as path
import shutil
import datetime
import stat
import urllib2

git_clone_url_Path = 'git@github.com:haojiakang/sman.git'

script_name = 'sman'
bin_dir = '/usr/local/bin'
sman_dir = path.join(os.getcwd(), script_name)
bin_path = path.join(bin_dir, script_name)


def install():
    check_exists()
    __download()
    __do_install()


def check_exists(rm_direct=False):
    if not (path.exists(bin_path) and path.isfile(bin_path)):
        return

    install_dir = get_install_dir()
    if not install_dir:
        print('not found sman install dir in \'%s\'' % bin_path)
        os.remove(bin_path)
        exit(0)

    if not rm_direct:
        prompt = 'sman was already installed in \'%s\', remove it and reinstall in current dir?' % install_dir
        rm_direct = prompt_and_read_yes(prompt)
        if rm_direct:
            if sman_dir != install_dir and sman_dir.startswith(install_dir):
                print('installed dir contains cur work dir, can not be re installed')
                exit(0)

    if rm_direct:
        shutil.rmtree(install_dir)
        print('\'%s\' was removed.' % install_dir)
        os.remove(bin_path)
    else:
        print('you choose not to reinstall sman, terminated.')
        exit(0)


def get_install_dir():
    script_path = 'sman_path'
    with open(bin_path, 'r') as f:
        for line in f.readlines():
            if line.startswith(script_path):
                start_pot = len(script_path) + 4
                install_path = line[start_pot:-2]
                return path.dirname(install_path)


def __download():
    command = 'git clone %s --depth=1 "%s"' % (git_clone_url_Path, sman_dir)

    if path.exists(sman_dir) and path.isdir(sman_dir):
        prompt = 'destination path \'%s\' already exists, delete and continue?' % sman_dir
        if prompt_and_read_yes(prompt):
            shutil.rmtree(sman_dir)
            print('destination path \'%s\' removed' % sman_dir)
        else:
            print('install terminated')
            exit(0)

    os.system(command)


def prompt_and_read_yes(prompt):
    input_strs = ['y', 'n']

    while True:
        process = os.popen('read -p "%s" choice < /dev/tty && echo $choice' % (prompt + ' please input [y/n]: '))
        input_str = str.strip(str(process.read()))
        lower_input = str.lower(input_str)
        if lower_input not in input_strs:
            continue
        return lower_input == 'y'


def __do_install():
    sman_bin_path = path.join(bin_dir, script_name)
    sman_exec_path = path.join(sman_dir, script_name)

    sman_bin_content = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : {0}
# @Author  : jiakang
# @File    : sman
# @Software: IntelliJ IDEA

import os, sys

sman_path = '{1}'
command = 'python %s %s' % (sman_path, str.join(' ', sys.argv[1:]))
# print(command)
os.system(command)

'''.format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M'), sman_exec_path)
    # print(sman_bin_content)

    with open(sman_bin_path, 'w') as f:
        f.write(sman_bin_content)

    chmod_add_x(sman_bin_path)
    # chmod_add_x(sman_exec_path)

    walk_and_gen_tab_complete(sman_dir)
    __gen_complete_zsh_file()
    __gen_complete_bash_file()
    __gen_complete_chooser_file()

    prompt = '''
    
======================================================    
install complete. please add
    
    source %s/gen/sman-complete
    
to your .bashrc or .bash_profile to use auto complete.
======================================================
    ''' % sman_dir
    print(prompt)


def walk_and_gen_tab_complete(cur_sman_dir, truncate=False):
    scripts = __get_common_scripts(cur_sman_dir)
    # __walk_dir(path.join(cur_sman_dir, 'core'), scripts)
    # __walk_dir(path.join(cur_sman_dir, 'custom'), scripts)
    base_scripts_dirs = get_base_scripts_dirs(cur_sman_dir)
    # print(base_scripts_dirs)
    for base_scripts_dir in base_scripts_dirs:
        __walk_dir(path.join(cur_sman_dir, base_scripts_dir), scripts)

    custom_scripts_dirs = get_custom_scripts_dirs(cur_sman_dir)
    for custom_scripts_dir in custom_scripts_dirs:
        __walk_dir(path.join(cur_sman_dir, 'custom', custom_scripts_dir, 'scripts'), scripts)
    __gen_tab_complete(cur_sman_dir, scripts, truncate)


def get_base_scripts_dirs(cur_sman_dir):
    base_scripts_dirs = []
    all_dirs = os.listdir(cur_sman_dir)
    for dirname in all_dirs:
        if path.isdir(
                path.join(cur_sman_dir, dirname)) and dirname != 'gen' and dirname != 'test' and dirname != '.git' and dirname != 'custom':
            base_scripts_dirs.append(dirname)
    return base_scripts_dirs


def get_custom_scripts_dirs(cur_sman_dir):
    custom_scripts_dirs = []
    custom_dir = path.join(cur_sman_dir, 'custom')
    all_dirs = os.listdir(custom_dir)
    for dirname in all_dirs:
        if path.isdir(path.join(custom_dir, dirname)):
            custom_scripts_dirs.append(dirname)
    return custom_scripts_dirs


def __get_common_scripts(cur_sman_dir):
    common_scripts = []

    content_lines = []
    sman_common_path = path.join(cur_sman_dir, 'sman_common.py')
    if path.exists(sman_common_path) and path.isfile(sman_common_path):
        with open(sman_common_path) as f:
            content_lines = f.readlines()

    if content_lines:
        for line in content_lines:
            if line.startswith('def'):
                end = line.index('(')
                method_name = line[3:end].strip()
                if method_name != 'try_do_common' and not method_name.startswith('_'):
                    common_scripts.append(method_name)

    return common_scripts


def __walk_dir(dir_to_walk, scripts):
    if not (path.exists(dir_to_walk) and path.isdir(dir_to_walk)):
        print('dir_to_walk \'%s\' is not exists', dir_to_walk)
        return

    listdirs = os.listdir(dir_to_walk)
    for filename in listdirs:
        if path.isfile(path.join(dir_to_walk, filename)) and filename != '__init__.py' and not filename.startswith('_'):
            # chmod_add_x(path.join(dir_to_walk, filename))
            scripts.append(filename)


def __gen_tab_complete(cur_sman_dir, scripts, truncate):
    cmds_file = path.join(cur_sman_dir, 'gen', 'sman_cmds')
    with open(cmds_file, 'a') as f:
        if truncate:
            f.seek(0)
            f.truncate()
        for filename in scripts:
            f.write(filename)
            f.write(os.linesep)


def __gen_complete_zsh_file():
    content = '''#!/bin/zsh
### sman zsh complete

function listSmanCompletations {
    reply=(
    $(cat %s/gen/sman_cmds | xargs echo)
    )
}

compctl -K listSmanCompletations sman
    ''' % sman_dir
    with open(path.join(sman_dir, 'gen', 'complete.zsh'), 'w') as f:
        f.write(content)


def __gen_complete_bash_file():
    content = '''#!/bin/bash
### sman bash complete

function _sman_complete() {
    local pre cur opts
    COMPREPLY=()
    pre=${1}
    cur=${2}
    case "$cur" in
    * )
    cmds=$(cat %s/gen/sman_cmds | xargs echo)
        COMPREPLY=( $( compgen -W "$cmds" -- $cur ) )
    esac
}

export -f _sman_complete
complete -F _sman_complete -A file wtool
    ''' % sman_dir
    with open(path.join(sman_dir, 'gen', 'complete.bash'), 'w') as f:
        f.write(content)


def __gen_complete_chooser_file():
    content = '''#!/bin/bash
if [ -n "$ZSH_VERSION" ]; then
    source %s/gen/complete.zsh
else
    source %s/gen/complete.bash
fi
    ''' % (sman_dir, sman_dir)
    with open(path.join(sman_dir, 'gen', 'sman-complete'), 'w') as f:
        f.write(content)


# 赋予755权限
def chmod_add_x(file_to_ch):
    os.chmod(file_to_ch,
             stat.S_IRWXU |
             stat.S_IRGRP |
             stat.S_IXGRP |
             stat.S_IROTH |
             stat.S_IXOTH)


if __name__ == '__main__':
    install()
