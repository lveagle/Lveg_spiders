# -*- coding: utf-8 -*-

import json
import time
import redis
import os, os.path
import requests
import  random
import newspaper


class LvegspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class meizituPipeline(object):
    def open_spider(self, spider):
        image_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'image')
        if not os.path.exists(image_path):
            os.makedirs(image_path)
            os.chdir(image_path)
        else:
            os.chdir(image_path)

    def process_item(self, item, spider):
        with open(str(time.time())+'.jpg', 'wb') as f:
            f.write(requests.get(item['url']).content)

class qqwzPipeline(object):
    def open_spider(self, spider):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
        self.r = redis.StrictRedis(connection_pool=self.pool)

    def process_item(self, item, spider):
        # 保存的数据有空的，读取时要区分
        # 获取文章内容
        content, title = '', ''
        try:
            article = newspaper.Article(item['url'])
            article.download()
            article.parse()
            content = article.text
            title = article.title
        except:
            pass
        data = {
            'content': content,
            'title': title,
            'keywords': item['keywords'],
            'description': item['description']
               }
        self.r.lpush('qqwz', json.dumps(data))

class mashPipeline(object):
    # def open_spider(self, spider):
        # if not os.path.exists('mash_image'):
        #     os.mkdir('mash_image')

    def process_item(self, item, spider):
        # with open('mash_image\{}.jpg'.format(random.random()), 'wb+') as fp:
        #     fp.write(requests.get(item['url']).content)
        with open('url.txt', 'a+') as fp:
            fp.write(item['url'])
            fp.write('\n')


