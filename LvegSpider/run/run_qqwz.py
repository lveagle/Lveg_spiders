#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-08-09 20:23
"""
import time
import json
import redis
import random
import schedule
import threading
from LvegSpider.utils.auto_qqwz import  Auto_article

# connect to redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
r = redis.StrictRedis(connection_pool=pool)

def job():
    index = random.randint(0, int(r.llen('qqwz')))
    redis_data = r.lindex('qqwz', index)
    try:
        data = json.loads(redis_data)
    except Exception as e:
        print(e)
        return
    # r.lrem('qqwz', 0, redis_data)
    if data['content'] == '' or data['title'] == '':
        r.lrem('qqwz', 0, redis_data)
        return
    else:
        try:
            A = Auto_article(data['content'], data['title'], data['description'], data['keywords'])
            A.publish()
        except Exception as e:
            print(e)
            pass
        finally:
            r.lrem('qqwz', 0, redis_data)


# def run_threaded(job_func):
#     job_thread = threading.Thread(target=job_func)
#     job_thread.start()

# schedule.every(20).minutes.do(run_threaded, job)
# schedule.every(20).minutes.do(job)
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
