# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpecItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    name = scrapy.Field()
    spec = scrapy.Field()


class MediaItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
