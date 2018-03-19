# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import pandas as pd
from lxml import etree


def getHtmlText(url):
    try:
        rr = requests.get(url, timeout=20)
        rr.raise_for_status()
        rr.encoding = rr.apparent_encoding
        return r.text
    except Exception as e:
        print(e)
        return str(e)

if __name__ == '__main__':
    url = "https://book.douban.com/subject/5409459/comments/"
    # s = etree.HTML(getHtmlText(url))
    r = requests.get(url).text
    s = etree.HTML(r)
    # print(s.xpath('//*[@id="comments"]/ul/li[1]/div[2]/p/text'))
    file = s.xpath('//span[@class="comment-info"]/a/text()')

    df = pd.DataFrame(file)
    df.to_excel('pinglun.xlsx')
