# -*- coding: utf-8 -*-
import re

import scrapy

from ..items import FangItem


class SwfSpider(scrapy.Spider):
    name = 'swf'
    allowed_domains = ['fang.com']
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

        div_list=response.xpath('//div[@id="newhouse_loupai_list"]//div[@class="nlc_details"]')

        for div in div_list:
            name=div.xpath('.//div[@class="nlcd_name"]/a/text()').extract_first().strip('\t\n')
            # .xpath('string(.)')意思是将标签中子标签的文本进行拼接
            # 他的调用者是seletor列表
            price = div.xpath('.//div[@class="nhouse_price"]')
            #判断在页面中获取到“class="nhouse_price”是否有值，例如：“价格待定”，标签值就变了
            if price:
                price=price.xpath('string(.)').extract_first().strip('\t\n').strip('广告').strip('\t\n')

            fang['name']=name
            fang['price']=price
            yield fang

            # 尾页的href的值  last() 就是xpath中获取最后一个数据的方法
            href = response.xpath('//a[@class="last"][last()]/@href').extract_first()
            # 有的城市只有一页 就不需要执行以下代码了
            if href:
                # /house/s/b932/
                reg='/b9(\d+)/'
                pattern = re.compile(reg)
                # 尾页的数据拿到
                num= pattern.findall(href)[0]
                # https://newhouse.fang.com/house/s/
                url = response.url
                # https://newhouse.fang.com/house/s/b92/
                # 3
                # 当前页 + 1   尾页  page是当前页的页码
                page = pattern.findall(url)
                if len(page) == 0:
                    page = 2
                else:
                    page = int(page[0]) + 1
                url1 = response.meta['url']
                for i in range(page,int(num)+1):
                    url=url1 + 'b9' +str(i) + '/'
                    yield scrapy.Request(url=url,callback=self.parseSecond,meta={'fang':fang,'url':url1})
                    break
