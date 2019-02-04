# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LvegspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class qqwzItem(Item):
    # 用作网站千千网赚的文章
    # content = Field()
    # title = Field()
    url = Field()
    description = Field()
    keywords = Field()


class mashItem(Item):
    url = Field()

