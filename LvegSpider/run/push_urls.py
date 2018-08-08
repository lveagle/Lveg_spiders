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
        "meizitu:start_urls":["http://www.meizitu.com/a/more_1.html"],
        # "finance_ifeng:start_urls":['http://finance.ifeng.com/',
        #                             'http://tech.ifeng.com/',
        #                              'http://finance.ifeng.com/stock/gstzgc/'],
        }


for key, start_urls in spiders_dict.items():
    for url in start_urls:
        r.lpush(key, url)