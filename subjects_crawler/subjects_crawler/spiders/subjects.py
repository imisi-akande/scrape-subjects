# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

class SubjectsSpider(Spider):
    name = 'subjects'
    allowed_domains = ['classcentral.com/subjects']
    start_urls = ['https://classcentral.com/subjects/']

    def parse(self, response):
        pass
