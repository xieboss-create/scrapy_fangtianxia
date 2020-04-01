# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings


class FangPipeline(object):
    def open_spider(self, spider):
        self.fp = open('fang.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item

    def close_spider(self, spider):
        self.fp.close()


class SaveDataPipeline(object):
    def open_spider(self, spider):
        # 会把settings中的所有的等号左边的值当作key  等号右边的值当作value
        settings = get_project_settings()
        db_host = settings['DB_HOST']
        db_port = settings['DB_PORT']
        db_user = settings['DB_USER']
        db_password = settings['DB_PASSWORD']
        db_name = settings['DB_NAME']
        db_charset = settings['DB_CHARSET']

        self.conn = pymysql.Connect(host=db_host,
                                    user=db_user,
                                    password=db_password,
                                    database=db_name,
                                    # 端口号必须是整型
                                    port=db_port,
                                    # 字符集不允许加-
                                    charset=db_charset)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # {}的外面必须要加 “”
        sql = 'insert into `fangtianxia` values ("{}","{}","{}","{}")'.format(item['province'], item['city'],
                                                                              item['name'], item['price'])
        self.cursor.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
