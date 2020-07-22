# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DmzjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #图片链接
    pic_urls = scrapy.Field()
    #章节名
    title = scrapy.Field()
    #漫画名
    big_title = scrapy.Field()
