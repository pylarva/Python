# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from scrapy.http import Request
from scrapy.http.cookies import CookieJar
from scrapy.selector import Selector


class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['http://chouti.com/']
    cookie_dict = {}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, callback=self.parse1)

    def parse1(self, response):
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)

        for k, v in cookie_jar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value

        post_dict = {
            'phone': '8618550119027',
            'password': 'li123456',
            'oneMonth': 1
        }

        yield Request(
            url="http://dig.chouti.com/login",
            method='POST',
            cookies=self.cookie_dict,
            # 用urllib模块将字典拼接成 k1=v1&k2=v2
            body=urllib.parse.urlencode(post_dict),
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            callback=self.parse2
        )

    def parse2(self, response):
        print(response.text)
        yield Request(url='http://dig.chouti.com/', cookies=self.cookie_dict, callback=self.parse3)

    def parse3(self, response):
        hxs = Selector(response)

        # 点赞
        link_id_list = hxs.xpath('//div[@class="part2"]/@share-linkid').extract()
        for link_id in link_id_list:
            base_url = "http://dig.chouti.com/link/vote?linksId=%s" % link_id
            yield Request(base_url, cookies=self.cookie_dict, method='POST', callback=self.parse4)

        # 翻页
        page_list = hxs.xpath("//div[@id='page-area']//a/@href").extract()
        for page in page_list:
            page_url = 'http://dig.chouti.com%s' % page
            yield Request(url=page_url, method='GET', cookies=self.cookie_dict, callback=self.parse3, dont_filter=True)

    def parse4(self, response):
        print(response.text)

    def parse(self, response):
        hxs = Selector(response)

        from ..items import Sp2Item

        # 标题
        title_content = hxs.xpath("//div[@class='part2']")
        for title in title_content:
            t = title.xpath('./@share-title').extract_first()
            z = title.xpath('./a/b/text()').extract_first()
            yield Sp2Item(title=t, zan=z)

