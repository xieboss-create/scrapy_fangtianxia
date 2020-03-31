# -*- coding: utf-8 -*-
import scrapy


class SwfSpider(scrapy.Spider):
    name = 'swf'
    allowed_domains = ['https://www.fang.com/SoufunFamily.htm']
    start_urls = ['http://https://www.fang.com/SoufunFamily.htm/']

    def parse(self, response):
        pass
