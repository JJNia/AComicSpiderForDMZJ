# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
from scrapy.utils.project import get_project_settings
import pymysql
class DmzjPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        host = settings["MYSQL_HOST"]
        port = settings["MYSQL_PORT"]
        user = settings["MYSQL_USER"]
        passwd = settings["MYSQL_PASSWORD"]
        dbname = settings["MYSQL_DBNAME"]
        charset = settings["MYSQL_CHARSET"]
        print (host, port, user, passwd, dbname, charset)
        self.db = pymysql.connect(host=host, port=port, user=user, passwd= passwd, db=dbname, charset=charset)
        self.cur = self.db.cursor()
        self.cur.execute('TRUNCATE TABLE capter')
        self.db.commit()


    def process_item(self, item, spider):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'cookie': 'UM_distinctid=16706eb86dcd8-02bc2f02cd5057-333b5602-100200-16706eb86dd6e5; bdshare_firstime=1542009358470; laravel_session=eyJpdiI6InJZMTQrZFlRVFphOVlXU2R0dFwvRnl3PT0iLCJ2YWx1ZSI6IjFJZGdacHA5YkJSRzhHSWJoVklwaTNiaTl0dHRCMzFwSzRGT0oxWm81MXl5aGtkT0lDVHFQRTlBcUJkN3hEQ2xWXC9yZWRxbjJzNSthVWg2VFBVbXRUZz09IiwibWFjIjoiZmZiY2Q0YjkyZTAwMzBjNDk4YjAwZmVkYTg1NzY3NmY4MzU5YjM2NjQzZTdlNTExMWI3ZmJiYTMyNjhlN2YwMSJ9; CNZZDATA1255781707=1633799429-1542006327-%7C1542011727; CNZZDATA1000465408=1899900830-1542005345-%7C1542012974',
            'referer': 'https://m.dmzj.com/info/zuizhongwochengleni.html'
        }

        # 确认漫画的目录是否存在 manhua_name:该漫画的名称
        manhua_name = os.path.join(r'C:\Users\30263\Desktop', item['big_title'])
        # 若不存在，则添加文件夹
        if not os.path.exists(manhua_name):
            os.mkdir(manhua_name)
        # 确认每一话的目录是否存在 catapot_name:该章节的名称
        catapot_name = os.path.join(manhua_name, item['title'])
        # 若不存在，则添加文件夹
        if not os.path.exists(catapot_name):
            os.mkdir(catapot_name)

        for pic_url in item['pic_urls']:
            title = item['title']
            big_title = item['big_title']

            capter = pic_url.split('/')[-1]
            #返回字节流
            response = requests.get(pic_url, headers=headers).content
            with open(catapot_name + r'\\' + capter, 'wb') as fp:
                fp.write(response)
                fp.close()
                print("正在下载" + item['big_title'] + " " + item['title'] + " " + capter)
            self.cur.execute('INSERT INTO capter(catapot_name, capter_name, comic_name, capter_file) VALUES(%s, %s, %s, %s)', (str(title), str(capter), str(big_title), str(response)))
            self.db.commit()
        return item
