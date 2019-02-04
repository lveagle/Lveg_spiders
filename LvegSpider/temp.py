#!/usr/bin/env python
# -*- coding: utf-8 -*-



# from LvegSpider.utils.send_to_qq import send_to_qq
# send_to_qq('helol test again')

# """
import redis
import json
from lveg.common_funcs import *
import random

"""
# connect to redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
r = redis.StrictRedis(connection_pool=pool)

index_list = list(range(int(r.llen('qqwz'))))
# index = random.randint(0, int(r.llen('qqwz')))
# data = json.loads(r.lpop('qqwz_1:items'))
# data = json.loads(r.lindex('qqwz', 1020))
# data = json.loads(r.lindex('qqwz', index))

for index in index_list:
# for index in [0,1,2,3,4]:
    try:
        redis_data = r.lindex('qqwz', index)
        data = json.loads(redis_data)
        if data['content'] == '' or data['title'] == '':
            r.lrem('qqwz', 0, redis_data)
    except:
        continue
"""
import requests
from urllib.request import urlretrieve
import multiprocessing
import os, os.path

if __name__ == '__main__':

    if not os.path.exists('dnf_image'):
        os.mkdir('dnf_image')

    pool = multiprocessing.Pool(processes=4)
    with open('url.txt') as fp:
        data = fp.readlines()
    for count, url in enumerate(data):
        pool.apply_async(urlretrieve, (url, 'dnf_image/'+str(count)+'.jpg', ))
    pool.close()
    pool.join()


