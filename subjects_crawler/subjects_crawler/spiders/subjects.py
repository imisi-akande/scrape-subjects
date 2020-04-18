# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import logging
logger = logging.getLogger('subjectslogger')

class SubjectsSpider(Spider):
    name = 'subjects'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://classcentral.com/subjects']

    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath('//a[contains(@title, "'+ self.subject +'")]/@href').extract_first()
            absolute_subject_url = response.urljoin(subject_url)
            yield Request(absolute_subject_url, callback = self.parse_subject)
        else:
            logger.info('Scraping all subjects......... %s', response.url)
            subjects = response.xpath('//h3/a[1]/@href').extract()
            for subject in subjects:
                absolute_subject_url = response.urljoin(subject)
                yield Request(absolute_subject_url, callback=self.parse_subject)


    def parse_subject(self, response):
        subject_title = response.xpath('//h1/text()').extract_first()
        subject_description = response.xpath('//p[@class="text-1"]/text()').extract_first()
        subject_followers = response.xpath('//button[@data-name="FOLLOW"]/span/text()').extract_first()
        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')

        for course in courses:
            course_title = course.xpath('.//span[@itemprop="name"]/text()').extract_first().strip()
            start_date = course.xpath('.//td[@itemprop="startDate"]/text()').extract_first()
            course_url = course.xpath('.//a[@itemprop="url"]/@href').extract_first()
            absolute_course_url = response.urljoin(course_url)

            yield{"subject_title": subject_title,
                  "course_title":course_title,
                  "start_date": start_date,
                  "subject_description": subject_description,
                  "subject_followers": subject_followers,
                  "absolute_course_url":absolute_course_url}

        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_page:
            absolute_next_page = response.urljoin(next_page)
            yield Request(absolute_next_page, callback=self.parse_subject)
