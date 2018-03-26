# !/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy import Selector
from pyquery import PyQuery

with open('index.html', encoding='utf-8') as f:
    text = f.read()

# sel = Selector(text=text)
# s = sel('.top')
# print(sel.xpath('/html/body/ul/li')[0].xpath('./@class').extract_first())

pq = PyQuery(text)
# print(pq('li div').text())
# print(pq('.top').attr('class'))