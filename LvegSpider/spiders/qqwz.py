#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__: Lveg 
__time__: 2018-08-08 23:44
爬取各类博客上的文章，然后自动发布到我的网站
"""

import newspaper
from LvegSpider.spiders.demo import *
from scrapy.linkextractors import LinkExtractor

class qqwz_1(RedisCrawlSpider):
    name = 'qqwz_1'
    redis_key = 'qqwz_1:start_urls'
    allowed_domains = ['shangmeidd.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "LvegSpider.middlewares.UserAgentMiddleware": 401,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'LvegSpider.middlewares.IProxyMiddleware': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.SpiderPriorityQueue',
        'SCHEDULER_PERSIST' : True,

        'ITEM_PIPELINES' : {
           'scrapy_redis.pipelines.RedisPipeline': 300,
           'LvegSpider.pipelines.qqwzPipeline': 301,
        },
        'REDIS_HOST' : '127.0.0.1',
        'REDIS_PORT': 6379,
        'LOG_LEVEL' :'DEBUG',
        #默认情况下,RFPDupeFilter只记录第一个重复请求。将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
        'DUPEFILTER_DEBUG': True,
    }
    rules = (
        Rule(LinkExtractor(allow=(r'/page/\d+', )), follow=True) ,
        Rule(LinkExtractor(allow=(r'.com/\d+', )), callback='parse_item', follow=True) ,
    )

    def parse_item(self, response):
        item = qqwzItem()
        item['url'] = response.url
        # 获取关键字和描述
        try:
            item['keywords'] = response.css('meta[name="keywords"]::attr(content)').extract()[0]
            item['description'] = response.css('meta[name="description"]::attr(content)').extract()[0]
        except:
            item['keywords'] = ''
            item['description'] = ''
        yield item


class qqwz_2(RedisCrawlSpider):
    name = 'qqwz_2'
    redis_key = 'qqwz_2:start_urls'
    allowed_domains = ['fububu.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "LvegSpider.middlewares.UserAgentMiddleware": 401,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'LvegSpider.middlewares.IProxyMiddleware': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.SpiderPriorityQueue',
        'SCHEDULER_PERSIST' : True,

        'ITEM_PIPELINES' : {
           'scrapy_redis.pipelines.RedisPipeline': 300,
           'LvegSpider.pipelines.qqwzPipeline': 301,
        },
        'REDIS_HOST' : '127.0.0.1',
        'REDIS_PORT': 6379,
        'LOG_LEVEL' :'DEBUG',
        #默认情况下,RFPDupeFilter只记录第一个重复请求。将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
        'DUPEFILTER_DEBUG': True,
    }

    rules = (
        Rule(LinkExtractor(allow=(r'catalog.asp?page=\d+', )),  follow=True),
        Rule(LinkExtractor(allow=(r'view/\d+.html', )), callback='parse_item', follow=True) ,
    )

    def parse_item(self, response):
        item = qqwzItem()
        item['url'] = response.url
        #获取关键字和描述
        try:
            item['keywords'] = response.css('meta[name="keywords"]::attr(content)').extract()[0]
            item['description'] = response.css('meta[name="description"]::attr(content)').extract()[0]
        except:
            item['keywords'] = ''
            item['description'] = ''
        yield item

class qqwz_3(RedisCrawlSpider):
    name = 'qqwz_3'
    redis_key = 'qqwz_3:start_urls'
    allowed_domains = ['jiankeba.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "LvegSpider.middlewares.UserAgentMiddleware": 401,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'LvegSpider.middlewares.IProxyMiddleware': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.SpiderPriorityQueue',
        'SCHEDULER_PERSIST' : True,

        'ITEM_PIPELINES' : {
           'scrapy_redis.pipelines.RedisPipeline': 300,
           'LvegSpider.pipelines.qqwzPipeline': 301,
        },
        'REDIS_HOST' : '127.0.0.1',
        'REDIS_PORT': 6379,
        'LOG_LEVEL' :'DEBUG',
        #默认情况下,RFPDupeFilter只记录第一个重复请求。将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
        'DUPEFILTER_DEBUG': True,
    }

    """ 
    /wangzhuanjingyan/p5/
   /youxizhuanqian/1131.html 
    """

    rules = (
        Rule(LinkExtractor(allow=(r'/\w+/p\d+/', )),  follow=True),
        Rule(LinkExtractor(allow=(r'/\w+/\d+.html', )), callback='parse_item') ,
    )

    def parse_item(self, response):
        item = qqwzItem()
        item['url'] = response.url
        # 获取关键字和描述
        try:
            item['keywords'] = response.css('meta[name="keywords"]::attr(content)').extract()[0]
            item['description'] = response.css('meta[name="description"]::attr(content)').extract()[0]
        except:
            item['keywords'] = ''
            item['description'] = ''
        yield item

class auto_traffic(CrawlSpider):
    # 自动刷流量程序
    name = 'auto_traffic'
    allowed_domains = ['qqwz.site']
    start_urls = ['http://qqwz.site']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "LvegSpider.middlewares.UserAgentMiddleware": 401,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'LvegSpider.middlewares.IProxyMiddleware': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': 'auto_traffic.log',
        'DOWNLOAD_DELAY': 1,
    }
    rules = (
        Rule(LinkExtractor(allow=(r'/page/\d+/', )),  follow=True),
        Rule(LinkExtractor(allow=(r'archives/\d+', )), callback='parse_item', follow=True) ,
    )

    def parse_item(self, response):
        yield None


# 接下来的网址
# http://www.xiaozhuan5.com/
# http://www.lichangtao.com/page_7.html
