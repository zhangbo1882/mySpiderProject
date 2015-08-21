__author__ = 'Aaron'
#coding:utf-8
from scrapy.http import Request
#from scrapy.spiders import Spider
from scrapy.selector import Selector
#from scrapy.statscollectors import MemoryStatsCollector
from mySpiderProject.items import zhihuUser
from scrapy_redis.spiders import  RedisSpider

class zhihuSpider(RedisSpider):
    name = "zhihu_dist"

    '''
    The password is encrypted in javascript. So this way can not login with user/password
    def post_login(self, response):
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print xsrf
        return scrapy.FormRequest.from_response(response, meta={'cookiejar':1}, formdata={'_xsrf':xsrf,'account':'zhangbo1882@163.com', 'password':'zhangbo'}, callback=self.after_login)
    '''
    headers = {'Accept-Encoding':'deflate',
               'Accept-Language':'zh-CN,zh;en-Us,en',
   }
    base_url = 'http://www.zhihu.com'
    user_list=[]
    MAX_USER=1000

    def start_requests(self):

        return [Request(self.base_url,
                        meta={'cookiejar':1},
                        headers=self.headers,
                        cookies={'__utma':'51854390.1558793268.1438675869.1438675869.1438675869.1',
                                 '__utmb':'51854390.4.10.1438675869',
                                 '__utmc':'51854390',
                                 '_za':'713ffd97-50d8-493c-b483-4dcb978d6fd9',
                                 '__umt':'1',
                                 'q_c1':'d83e66a34d2c47f6aa1687bb31dd5012|1438675947000|1438675947000',
                                 'cap_id':'"MjI3ZWYyYzI0ZGRjNDkwMzgyMWM2NzA3Yjc0ZWVmODg=|1438675947|c676a11c494e528907bd0828c380ce6731b55668"',
                                 'z_c0':'"QUJDTVVQa3RiQWdYQUFBQVlRSlZUZjRBNkZXU0JaNXpEcWFNT3RkVHdPRUpsV2dwbnk2cWtRPT0=|1438675966|4757fe838704cc65de5639fc3954f09921ca1572"',
                                 'unlock_ticket':'"QUJDTVVQa3RiQWdYQUFBQVlRSlZUUVo3d0ZVSXYzTHdFSTROMW9ZSndXNkZhVVFQbmszdExnPT0=|1438675966|ca5ded08e0a0b67aca91bb32a7acdd37ce5b9246"',
                                 '_xsrf':'c518c0f203ebac2dcdc7d3e09cc0ab1b',
                                 '__utmz':'51854390.1438675869.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
                                 '__utmv':'51854390.100-2|2=registration_date=20150721=1^3=entry_date=20150721=1'
                                },
                        callback=self.after_login)]

    def parse(self, response):
        pass

    def process_about(self, response):
        item = zhihuUser()
        if len(self.user_list) > self.MAX_USER:
            print("Exceed max user %d"%len(self.user_list))
            self.crawler.stop()
            return
        #get followee
        urlName = response.url.split("/")[-2]
        yield Request(self.base_url+'/people/'+ urlName+ '/followees', meta={'cookiejar':response.meta['cookiejar']}, callback=self.process_followee)
        #handle item
        name = Selector(response).xpath('//a[@class="name"]/text()').extract()
        location = Selector(response).xpath('//span[@class="location item"]/text()').extract()
        business = Selector(response).xpath('//span[@class="business item"]/text()').extract()
        employ = Selector(response).xpath('//span[@class="employment item"]/text()').extract()
        education = Selector(response).xpath('//span[@class="education item"]/text()').extract()
        education_extra = Selector(response).xpath('//span[@class="education-extra item"]/text()').extract()
        if not location:
            location = Selector(response).xpath('//span[@class="location item"]/a/text()').extract()
        if not employ:
            employ = Selector(response).xpath('//span[@class="employment item"]/a/text()').extract()
        if not business:
            business = Selector(response).xpath('//span[@class="business item"]/a/text()').extract()
        if not education:
            education = Selector(response).xpath('//span[@class="education item"]/a/text()').extract()
        if not education_extra:
            education_extra = Selector(response).xpath('//span[@class="education-extra item"]/a/text()').extract()

        if location:
            item['location'] = location[0].encode("utf-8")
        else:
            item['location'] = ''
        if employ:
            item['employ'] = employ[0].encode("utf-8")
        else:
            item['employ'] = ''
        if business:
            item['business'] = business[0].encode("utf-8")
        else:
            item['business'] = ''
        if name:
           item['name'] = name[0].encode("utf-8")
        else:
            item['name'] = ''
        if education:
            item['education'] = education[0].encode("utf-8")
        else:
            item['education'] = ''
        if education_extra:
            item['education_extra'] = education_extra[0].encode("utf-8")
        else:
            item['education_extra'] = ''
        if item['name'] not in self.user_list:
            self.user_list.append(item['name'])

        yield item

    def process_followee(self, response):
        path = '//div[@class="zm-profile-card zm-profile-section-item zg-clear no-hovercard"]/div[@class="zm-list-content-medium"]/h2/a/'
        followeesUrl = Selector(response).xpath(path+'@href').extract()
        for url in followeesUrl:
            userName = url.split("/")[-1]
            if userName.encode("utf-8") not in self.user_list:
                yield Request(url+'/about', meta={'cookiejar':response.meta['cookiejar']}, callback=self.process_about)
            else:
                #print("%s has been crawled"%userName)
                pass
        pass


    def after_login(self, response):
        yield Request(self.base_url+'/people/zhangbo1882/about',  meta={'cookiejar':response.meta['cookiejar']}, callback=self.process_about)
        yield Request(self.base_url+'/people/zhangbo1882/followees', meta={'cookiejar':response.meta['cookiejar']}, callback=self.process_followee)
        #print response.body
        pass