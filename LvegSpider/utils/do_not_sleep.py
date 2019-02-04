#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-08-09 12:52
"""
import time
import random
from pymouse import PyMouse
from pykeyboard import PyKeyboard

mouse = PyMouse()
keyboard = PyKeyboard()
pos = ()
while True:
    try:
        pos = (random.randint(0, 1920), random.randint(0, 1080))
        mouse.move(*pos)
        # keyboard.tab_key(keyboard.up_key)
        keyboard.press_key(keyboard.space_key)
        time.sleep(60)
    except Exception as e:
        print(e)
        pass



