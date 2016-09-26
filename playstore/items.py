# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlaystoreItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()
    Developer = scrapy.Field()
    Downloads = scrapy.Field()
    LastUpdate = scrapy.Field()
    Size = scrapy.Field()
    Version = scrapy.Field()
    andriodRequirements = scrapy.Field()
    DeveloperLink = scrapy.Field()
    Rating = scrapy.Field()
    ratingCount = scrapy.Field()
    Description = scrapy.Field()
    Permissions = scrapy.Field()
