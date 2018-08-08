# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import os
import random
import redis
import json
import logging
import requests
from scrapy import signals
from LvegSpider.utils.user_agents import agents
from LvegSpider.utils.cookies import *
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class LvegspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgentMiddleware(object):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

        request.headers["Referer"] = request.url


class CookiesMiddleware(RetryMiddleware):

    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        self.rconn = redis.StrictRedis()
        self.site_key = crawler.settings.get('site_key')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        cookie = self.rconn.hget('cookies', self.site_key)

        if cookie and len(cookie) > 0:
            cookie = json.loads(cookie)
            request.cookies = cookie
        else:
            save_cookie('cookies', self.site_key, get_cookie(self.site_key))

class IProxyMiddleware(RetryMiddleware):
    # 重试用法
    # def __init__(self):
    #     RetryMiddleware.__init__(self)
    #     self.proxy = requests.get("http://127.0.0.1:5010/get/").content.decode()
    #
    # def process_request(self, request, spider):
    #     request.meta['proxy'] = "http://{}".format(self.proxy)
    #
    # def process_response(self, request, response, spider):
    #     if str(response.status).startswith('4'):
    #         self.proxy = requests.get("http://127.0.0.1:5010/get/").content.decode()
    #         request.meta['proxy'] = "http://{}".format(self.proxy)
    #
    #         return self._retry(request, spider)

    # 简单用法

    def process_request(self, request, spider):
        proxy = requests.get("http://127.0.0.1:5010/get/").content.decode()
        request.meta['proxy'] = "http://{}".format(proxy)



