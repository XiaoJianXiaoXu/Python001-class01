# -*- coding: utf-8 -*-

import scrapy
#from bs4 import BeautifulSoup
from scrapy.selector import Selector
from maoyanmovie.items import MaoyanmovieItem


class MaoyanSpider(scrapy.Spider):
   # 定义爬虫名称
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # 起始URL列表
    start_urls = ['https://maoyan.com']
    base_url = 'https://www.maoyan.com'
#   注释默认的parse函数
#   def parse(self, response):
#        pass


    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    # 解析函数
    def parse(self, response):
        #print(response.text)
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        #print(movies)
        for movie in movies[0:10]:
            link = movie.xpath("./a/@href")
            #print(link)
            detail_url = f'{self.base_url}{link.extract()[0]}'
            # print(detail_url)
            yield scrapy.Request(detail_url,callback=self.parse2)


    def parse2(self, response):

        details = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        items = []
        for detail in details:
            # 第一个取名字
            name = detail.xpath('./h1/text()').extract_first().strip()
            # li 集合
            li_elements = detail.xpath('./ul/li')
            print(li_elements)
            style = []
            # 第三个获取上映时间
            date = detail.xpath('./ul/li[3]/text()').extract_first().strip()
            # 类型比较麻烦，需要获取第一个li里的集合
            for key,value in enumerate(li_elements):
                if(key == 0):
                    for style_element in value.xpath('./a/text()'):
                        style.append(style_element.extract().strip())

            item = MaoyanmovieItem()
            item['movie_name'] = name
            item['movie_type'] = ",".join(style)
            item['movie_time'] = date
            items.append(item)

            yield item


