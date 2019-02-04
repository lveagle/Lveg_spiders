#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-08-05 3:54
"""

import redis

# connect to redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)

# start urls for each website
spiders_dict = {
        # "qqwz_1:start_urls": ['http://www.shangmeidd.com/page/1'],
        # "qqwz_2:start_urls": ['http://www.fububu.com/catalog.asp?page=1'],
        "qqwz_3:start_urls": [
            'http://www.jiankeba.com/wangzhuanjingyan/',
            'http://www.jiankeba.com/diaochazhuanqian/',
            'http://www.jiankeba.com/zhucezhuanqian/',
            'http://www.jiankeba.com/shoujizhuanqian/',
            'http://www.jiankeba.com/youxizhuanqian/',
            'http://www.jiankeba.com/touzizhuanqian/',
                              ],
        }

for key, start_urls in spiders_dict.items():
    for url in start_urls:
        r.lpush(key, url)