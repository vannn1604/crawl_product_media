# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
import json


class CrawlProductPipeline(object):
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host="172.17.0.2", database="tizzie", user="postgres", password="tizzie"
        )
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute(
            "insert into products(name,brand,spec) values(%s,%s,%s)",
            (item["name"], item["brand"], json.dumps(item["spec"]),),
        )
        self.connection.commit()
        print("----------------------------------------------------")
        return item

