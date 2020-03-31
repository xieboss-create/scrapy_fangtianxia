# -*- coding: utf-8 -*-
import scrapy

from ..items import FangItem


class SwfSpider(scrapy.Spider):
    name = 'swf'
    allowed_domains = ['https://www.fang.com/SoufunFamily.htm']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        tr_list = response.xpath('//div[@id="c02"]//tr')
        province_text = ''
        # 去除国外的城市
        for tr in tr_list[0:55]:
            province = tr.xpath('./td[2]//text()').extract_first().strip('\xa0')
            #给没有省份的市，添加省份
            if province:
                province_text = province
            else:
                province = province_text
            a_list = tr.xpath('./td[3]/a')

            for a in a_list:
                city=a.xpath('./text()').extract_first()


                if city =='北京':
                    url='https://newhouse.fang.com/house/s/'
                else:
                    href=a.xpath('./@href').extract_first()
                    url = href.split('.')[0]
                    url = url + '.newhouse.fang.com/house/s/'
                fang = FangItem(province=province, city=city)


                yield scrapy.Request(url=url,  meta={'fang':fang,'url':url},
                                     callback=self.parseSecond)
    def parseSecond(self,response):
        fang= response.meta['fang']