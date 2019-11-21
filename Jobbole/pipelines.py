# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
import redis



class MyMongodb():

    def __init__(self):

        #self.redis_url = 'redis://192.168.2.106'
        self.mongo_url = 'mongodb://127.0.0.1:27017'
        self.db = pymongo.MongoClient(self.mongo_url)

        #创建连接池
        # pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        # r = redis.StrictRedis(connection_pool=pool)

        self.r = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)





    def process_item(self, item, spider):
        db = self.db['Jobbole']
        sheet = db['jobbole']

        title_img = self.r.lpop('jobbole:items')
        print(title_img)
        sheet.insert(item)
        print("插入成功")

        return item
