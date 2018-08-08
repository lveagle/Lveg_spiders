# -*- coding: utf-8 -*-

import time
import os, os.path
import requests

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

