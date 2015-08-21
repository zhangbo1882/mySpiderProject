# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.extensions.corestats import CoreStats
from scrapy.statscollectors import DummyStatsCollector
class FilterWordsPipeline(object):

    def process_item(self, item, spider):
        print("print user info\n")
        print("用户名: %s"%item['name'])
        print("位置: %s"%item['location'])
        print("行业: %s"%item['business'])
        print("公司: %s"%item['employ'])
        print("学校: %s"%item['education'])
        print("专业: %s"%item['education_extra'])
        print('\n')




class MongoDBPipeline(object):
    def __init__(self):
        my_host = settings['MONGODB_SERVER']
        my_port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DB']
        client = pymongo.MongoClient(host=my_host, port=my_port)
        tdb = client[dbname]
        self.my_collection = tdb[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if item['name']:
            if not self.my_collection.find_one({"name":item['name']}):
                self.my_collection.insert(dict(item))
            else:
                print("%s exist in MongoDB"%item['name'])
        return item
        pass