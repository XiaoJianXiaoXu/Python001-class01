# -*- coding: utf-8 -*-

import scrapy
#from bs4 import BeautifulSoup
from scrapy.selector import Selector
from maoyanmovie.items import MaoyanmovieItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com']
    base_url = 'https://www.maoyan.com'

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        for movie in movies[0:10]:
            link = movie.xpath("./a/@href")
            detail_url = f'{self.base_url}{link.extract()[0]}'
            yield scrapy.Request(detail_url,callback=self.parse2)


    def parse2(self, response):

        details = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        items = []
        for detail in details:
            name = detail.xpath('./h1/text()').extract_first().strip()
            li_elements = detail.xpath('./ul/li')
            print(li_elements)
            style = []
            date = detail.xpath('./ul/li[3]/text()').extract_first().strip()
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


