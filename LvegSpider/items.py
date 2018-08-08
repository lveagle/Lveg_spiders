# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LvegspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZnGirlItem(scrapy.Item):
    name = scrapy.Field()
    pic_url = scrapy.Field(serializer=list)
    rate = scrapy.Field()


class meizituItem(scrapy.Item):
    url = scrapy.Field()

