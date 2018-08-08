#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-07-31 17:13
"""

import json
import scrapy
import collections
import logging
from LvegSpider.items import *
from scrapy_redis.spiders import RedisSpider

class Scrapy_redis_demo(RedisSpider):
    name = 'scrapy_redis'
    allowed_domains = ['meizitu.com']
    # start_urls = ['http://www.meizitu.com/a/more_1.html']

    redis_key = 'meizitu:start_urls'
    custom_settings = {
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.SpiderPriorityQueue',
        'SCHEDULER_PERSIST' : True,

        'ITEM_PIPELINES' : {
           'scrapy_redis.pipelines.RedisPipeline': 300, },
        'REDIS_HOST' : '127.0.0.1',
        'REDIS_PORT': 6379,
        'LOG_LEVEL' :'DEBUG',
        #默认情况下,RFPDupeFilter只记录第一个重复请求。将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
        'DUPEFILTER_DEBUG': True,
    }

    def parse(self, response):
        for url in  response.css('.wp-item a::attr(href)').extract():
            yield response.follow(url, callback=self.parse_pic)

        for url in response.css('#wp_page_numbers li a::attr(href)').extract():
            yield response.follow(url, callback=self.parse)

    def parse_pic(self, response):
        for url in response.css('#picture img::attr(src)').extract():
            print(url)
            yield None


