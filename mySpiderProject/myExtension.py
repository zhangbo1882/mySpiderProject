__author__ = 'Aaron'
class ExtensionGetStat(object):
    def __init__(self):
        print "hello"
    @classmethod
    def from_crawler(cls, crawler):
        print("from_crawler is called")
        pass