# -*- coding: utf-8 -*-
import time
import json
import scrapy
import collections
from LvegSpider.items import *
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response
from scrapy_splash import SplashRequest
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider
from LvegSpider.utils.cookies import  *
import random
import os, os.path


class User_agents_demo(scrapy.Spider):
    name = 'user_agent'
    allowed_domains = ['zhainanfulishe.com']
    start_urls = ['https://www.zhainanfulishe.com/nvshen']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "LvegSpider.middlewares.UserAgentMiddleware": 401,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        }
    }

    def parse(self, response):
        for url in response.css('article > a::attr(href)').extract():
            yield  response.follow(url, callback=self.parse_pic)

        next_page = response.css('span.pg-next a::attr(href)').extract_first()
        yield scrapy.Request(next_page, callback=self.parse)

    def parse_pic(self, response):
        print(response.request.headers['User-Agent'])
        yield None



class Ip_Proxy_demo(scrapy.Spider):
    name = 'ip_proxy'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            # 同时用上 user-agent
            "LvegSpider.middlewares.UserAgentMiddleware": 401,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'LvegSpider.middlewares.IProxyMiddleware': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
        'LOG_LEVEL': 'INFO'
    }

    """
    # 利用 user-agent 中的爬虫代码进行监测
    allowed_domains = ['zhainanfulishe.com']
    start_urls = ['https://www.zhainanfulishe.com/nvshen']
    def parse(self, response):
        for url in response.css('article > a::attr(href)').extract():
            yield  response.follow(url, callback=self.parse_pic)
        next_page = response.css('span.pg-next a::attr(href)').extract_first()
        yield scrapy.Request(next_page, callback=self.parse)

    def parse_pic(self, response):
        print(response.request.meta['proxy'], response.css('title::text').extract())
        yield None
    """

    # 新的检测方式, 可以工作
    # start_urls = ['http://ip111.cn/' for i in range(10)]
    # def parse(self, response):
    #     # self.logger.info(response.css('td')[4].css('td::text').extract_first().strip())
    #     print(response.css('td')[4].css('td::text').extract_first().strip())
    #     yield None

    start_urls = ['http://httpbin.org/ip' for i in range(10)]
    def parse(self, response):
        # print(response.css('td')[4].css('td::text').extract_first().strip())
        print(response.text)
        yield None




class Scrapy_splash_demo(scrapy.Spider):
    name = 'splash'
    start_urls = ["http://pvp.qq.com/web201605/wallpaper.shtml"]

    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        'DOWNLOADER_MIDDLEWARES':
            {
             'scrapy_splash.SplashCookiesMiddleware': 723,
             'scrapy_splash.SplashMiddleware': 725,
             'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            },
        'SPIDER_MIDDLEWARES':
            {
             'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
            },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url , self.parse , args={'wait': '0.5'} )
    def parse(self, response):
        print(response.css('#Work_List_Container_267733 div ul li.sProdImgDown.sProdImgL8 a::attr(rel)').extract())
        open_in_browser(response)
        yield item


class Link_demo(CrawlSpider):
    name = "link"
    start_urls = [
    ]

    custom_settings = {
    }

    rules = (
        Rule(LinkExtractor(allow=('/post\?page=\d+', )), follow=True),
        Rule(LinkExtractor(allow=('/post/show/\d+', )), callback='parse_pic', follow=True),
    )

    def parse_pic(self, response):
        print(response.css('img#image::attr(src)').extract_first())
        yield None


class Signin_demo(scrapy.Spider):
    name = 'sign_in'
    allowed_domains = ['1diaocha.com']
    start_urls = ['http://www.1diaocha.com/']
    custom_settings = {
        'site_key' : 'survey_1dc',
        'DOWNLOADER_MIDDLEWARES' : {
        'LvegSpider.middlewares.CookiesMiddleware': 402,
        },
        'LOG_LEVEL': 'INFO',
    }

    def parse(self, response):
        # 测试 是否登录，将默认处理函数作为一个跳板
        if not 'lvey' in response.text:
            save_cookie('cookies', self.custom_settings['site_key'], get_cookie(self.custom_settings['site_key']))
            self.logger.info('{} not login in'.format(self.custom_settings['site_key']))

        yield  Request(response.url, callback=self.real_parse)

    def real_parse(self, response):
        if 'lvey' in response.text:
            print('success login')
        else:
            print('failed login')
        # print(response.css('title::text').extract_first())
        yield None


# download mash
class Mash(CrawlSpider):
    name = "mash"
    start_urls = [
        # 'https://e-hentai.org/g/1277747/542e8e0f5b/',
        # 'https://e-hentai.org/g/1276767/149280ee4b/',
        # 'https://e-hentai.org/g/1276127/a3f26175f0/',
        # 'https://e-hentai.org/g/1276104/f838914444/',
        # 'https://e-hentai.org/g/1275525/647b708fae/',
        # 'https://e-hentai.org/g/1275265/3ec4463207/',
        # 'https://e-hentai.org/g/1274942/c154d4fd8d/',
        # 'https://e-hentai.org/g/1274903/6810de738c/',
        # 'https://e-hentai.org/g/1274404/f097c5de24/',
        # 'https://e-hentai.org/g/1271271/ed11a5a076/',
        # 'https://e-hentai.org/g/1271876/0dc613d698/',
        # 'https://e-hentai.org/g/1273371/94c9b34fc0/',
        # 'https://e-hentai.org/g/1269977/7e9f7ca0d7/',
        'https://e-hentai.org/g/1048750/7f747e4243/',
        'https://e-hentai.org/g/1022394/0645794bc9/',
        'https://e-hentai.org/g/1279394/1e118e1db0/',
        'https://e-hentai.org/g/1275211/c5828977e4/',
        'https://e-hentai.org/g/1191085/3edebb39dd/',
        'https://e-hentai.org/g/1104192/90920392dd/',
    ]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "LvegSpider.middlewares.UserAgentMiddleware": 401,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'LvegSpider.middlewares.IProxyMiddleware': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
        # 'ITEM_PIPELINES': {
        #     'LvegSpider.pipelines.mashPipeline': 310,
        # },
    }

    rules = (
        Rule(LinkExtractor(allow=(r'/?p=\d+', )), follow=True),
        Rule(LinkExtractor(allow=(r'https://e-hentai.org/s', )), callback='parse_pic'),
    )

    def parse_pic(self, response):
        url = response.css('img#img::attr(src)').extract_first()
        # yield scrapy.Request(url, callback=self.download)
        yield None
    #
    # def download(self, response):
    #     if not os.path.exists('dnf_image'):
    #         os.mkdir('dnf_image')
    #     with open('dnf_image/{}.jpg'.format(random.random()), 'wb+') as fp:
    #         fp.write(response.body)
    #

