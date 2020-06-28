#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/13 09:25
# @Author  : jiakang
# @File    : install.py
# @Software: IntelliJ IDEA

import os
import os.path as path
import shutil
import datetime, time
import pwd, stat, getpass

git_clone_url_path = 'git@github.com:haojiakang/sman.git'
script_name = 'sman'
bin_dir = '/usr/local/bin'
sman_dir = path.join(os.getcwd(), script_name)
bin_path = path.join(bin_dir, script_name)
sman_cfg_path = os.environ['HOME'] + '/.sman_config'

sman_auto_check_update_key = 'sman_auto_check_update'
sman_auto_check_update_value = 'true'
sman_prompt_update_verify_key = 'sman_promt_update_verify'
sman_prompt_update_verify_value = 'true'
sman_update_days_gap_key = 'sman_update_days_gap'
sman_update_days_gap_value = '14'
sman_last_update_day_key = 'sman_last_update_day'
sman_last_update_day_value = '0'


def install():
    check_exists()
    __download()
    __do_install()
    __do_sman_config()


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
        rm_direct = __prompt_and_read_yes(prompt)
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
    script_dir = 'sman_dir'
    with open(bin_path, 'r') as f:
        for line in f.readlines():
            if line.startswith(script_dir):
                start_pot = len(script_dir) + 4
                install_dir = line[start_pot:-2]
                return install_dir


def __download():
    command = 'git clone %s --depth=1 "%s"' % (git_clone_url_path, sman_dir)

    if path.exists(sman_dir) and path.isdir(sman_dir):
        prompt = 'destination path \'%s\' already exists, delete and continue?' % sman_dir
        if __prompt_and_read_yes(prompt):
            shutil.rmtree(sman_dir)
            print('destination path \'%s\' removed' % sman_dir)
        else:
            print('install terminated')
            exit(0)

    os.system(command)


def __prompt_and_read_yes(prompt):
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

    sman_bin_content = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : {0}
# @Author  : jiakang
# @File    : sman
# @Software: IntelliJ IDEA

import os, sys

sman_dir = '{1}'
sman_path = os.path.join(sman_dir, '{2}')
command = 'python %s %s' % (sman_path, str.join(' ', sys.argv[1:]))
# print(command)
os.system(command)

'''.format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M'), sman_dir, script_name)

    with open(sman_bin_path, 'w') as f:
        f.write(sman_bin_content)

    __chmod_add_x(sman_bin_path)

    walk_and_gen_tab_complete(sman_dir)
    __gen_complete_zsh_file()
    __gen_complete_bash_file()
    __gen_complete_chooser_file()

    prompt = '''
    
======================================================    
install complete. please add
    
source %s/gen/sman-complete
    
to your .bash_profile or .bashrc to use auto complete.
======================================================
    ''' % sman_dir
    print(prompt)


def __do_sman_config():
    sman_config_content = '''[sman]
sman_auto_check_update = true
sman_promt_update_verify = true
sman_update_days_gap = %s
sman_last_update_day = %s

''' % (sman_update_days_gap_value, get_current_day())

    if path.exists(sman_cfg_path) and path.isfile(sman_cfg_path):
        print('sman_cfg_path: %s already exists!' % sman_cfg_path)
        return

    with open(sman_cfg_path, 'w') as f:
        f.write(sman_config_content)
        print('sman_cfg_path: %s created!' % sman_cfg_path)


def get_current_day():
    now = time.time()
    return int(now) / 60 / 60 / 24


def walk_and_gen_tab_complete(cur_sman_dir, truncate=False):
    scripts = __get_common_scripts(cur_sman_dir)
    base_scripts_dirs = get_base_scripts_dirs(cur_sman_dir)

    for base_scripts_dir in base_scripts_dirs:
        __walk_dir(path.join(cur_sman_dir, base_scripts_dir), scripts)

    custom_scripts_dirs = get_custom_dirs(cur_sman_dir)
    for custom_scripts_dir in custom_scripts_dirs:
        __walk_dir(get_custom_scripts_dir(custom_scripts_dir), scripts)
    __gen_tab_complete(cur_sman_dir, scripts, truncate)


def get_base_scripts_dirs(cur_sman_dir):
    base_scripts_dirs = []
    all_dirs = os.listdir(cur_sman_dir)
    for dirname in all_dirs:
        if path.isdir(
                path.join(cur_sman_dir,
                          dirname)) and dirname != 'gen' and dirname != 'test' and dirname != '.git' and dirname != 'custom':
            base_scripts_dirs.append(dirname)
    return base_scripts_dirs


def get_custom_dirs(cur_sman_dir):
    custom_scripts_dirs = []
    custom_dir = path.join(cur_sman_dir, 'custom')
    all_dirs = os.listdir(custom_dir)
    for dirname in all_dirs:
        abs_dir_path = path.join(custom_dir, dirname)
        if path.isdir(abs_dir_path):
            custom_scripts_dirs.append(abs_dir_path)
    return custom_scripts_dirs


def get_custom_scripts_dir(custom_dir_path):
    return path.join(custom_dir_path, 'scripts')


# 判断脚本是否应当被sman收录
def should_script_gather_with_sman(script_path, filename):
    if path.exists(script_path) \
            and path.isfile(script_path) \
            and filename != '__init__.py' \
            and filename != 'README.md' \
            and not filename.startswith('_') \
            and __is_executable(script_path):
        return True
    return False


# 判断当前登录用户对于某文件是否具有可执行权限
def __is_executable(path):
    user = getpass.getuser()
    user_info = pwd.getpwnam(user)
    uid = user_info.pw_uid
    gid = user_info.pw_gid
    s = os.stat(path)
    mode = s[stat.ST_MODE]
    return (
            ((s[stat.ST_UID] == uid) and (mode & stat.S_IXUSR > 0)) or
            ((s[stat.ST_GID] == gid) and (mode & stat.S_IXGRP > 0)) or
            (mode & stat.S_IXOTH > 0)
    )


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
        print('dir_to_walk \'%s\' is not exists' % dir_to_walk)
        return

    listdirs = os.listdir(dir_to_walk)
    for filename in listdirs:
        script_path = path.join(dir_to_walk, filename)
        if should_script_gather_with_sman(script_path, filename):
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
complete -F _sman_complete -A file sman
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


# 添加可执行权限
def __chmod_add_x(file_to_ch):
    os.system('chmod +x %s' % file_to_ch)


if __name__ == '__main__':
    install()
