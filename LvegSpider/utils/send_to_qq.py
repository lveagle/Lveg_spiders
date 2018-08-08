#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-08-04 23:04
确保 qqbot 服务在运行，并且已经登录
"""

import subprocess


send_group_message = ('qq', 'send', 'group', 'qq-test')

def send_to_qq(message:str):
    subprocess.Popen([*send_group_message, message])
