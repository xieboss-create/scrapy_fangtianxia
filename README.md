# scrapy_redis_fangtianxia
爬取房天下，全国所有省市，楼盘的信息
包括：省，市，楼盘名，房价
最后保存到数据库中

克隆到本地后，
1.先安装requirements.txt中的依赖
2.修改settings.py文件中的database的配置，将DB_USER，DB_PASSWORD，DB_NAME修改为自己的
3.创建表和字段province，city，name，price，都为varchar（255）
