# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field

class zhihuUser(Item):
    name = Field()
    location = Field()
    business = Field()
    employ = Field()
    education = Field()
    education_extra = Field()