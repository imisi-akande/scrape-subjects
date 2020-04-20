# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging

import pymongo

logger = logging.getLogger('mongodblogger')

class MongoDBPipeline(object):

    collection_name = 'subjects'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, subjects_crawler):
        ## extract database information from settings.py
        return cls(
            mongo_uri=subjects_crawler.settings.get('MONGO_URI'),
            mongo_db=subjects_crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each item; subjects and courses
        self.db[self.collection_name].insert(dict(item))
        logger.info("Course added to MongoDB")
        return item
