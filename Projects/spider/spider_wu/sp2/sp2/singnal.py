# !/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy import signals


class MyExtension(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_crawler(cls, crawler):
        val = crawler.settings.getint('MMMM')
        ext = cls(val)

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        return ext

    def spider_opened(self, spider):
        print('open')

    def spider_closed(self, spider):
        print('close')