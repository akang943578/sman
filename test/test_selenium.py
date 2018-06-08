#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 10:52
# @Author  : jiakang
# @File    : test_selenium.py
# @Software: IntelliJ IDEA

from selenium import webdriver

import time

dr = webdriver.Chrome(executable_path='../core/__chromedriver')
dr.get('https://x.sankuai.com/')
# time.sleep(5)
# print('Browser will close')
# dr.quit()
# print('Browser closed')

# scriptArray = """localStorage.setItem("key1", 'new item');
#                localStorage.setItem("key2", 'second item');
# 				return Array.apply(0, new Array(localStorage.length)).map(function (o, i) { return localStorage.getItem(localStorage.key(i)); }
# 				)"""
time.sleep(20)
scriptArray = '''
u = localStorage.getItem('u')
dt = localStorage['dt']
return 'u: ' + u + ', dt: ' + dt
'''
result = dr.execute_script(scriptArray)
print(result)
