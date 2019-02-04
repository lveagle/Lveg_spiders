#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-08-09 21:26
"""
import time
import schedule
import threading
from scrapy import cmdline
import subprocess

# def job():
#     cmdline.execute("scrapy crawl auto_traffic".split())
#
# def run_threaded(job_func):
#     job_thread = threading.Thread(target=job_func)
#     job_thread.start()
#
# schedule.every(10).minutes.do(run_threaded, job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

while True:
    subprocess.Popen(['scrapy', 'crawl', 'auto_traffic'], shell=True)
    time.sleep(5*60)
