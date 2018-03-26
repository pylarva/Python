# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..utils.parse import parse, \
    xiaoqu_parse, get_ershou_price_list, \
    chuzu_list_pag_get_detail_url,\
    get_chuzu_house_info
from ..items import City58ItemXiaoQu, City58ItemXiaoChuZuQuInfo
from traceback import format_exc


class SpiderCity59Spider(scrapy.Spider):
    name = 'spider_city_59'
    allowed_domains = ['58.com']
    host = 'cd.58.com'
    xianqu_url_format = 'http://{}/xiaoqu/{}/'
    xianqu_code = list()
    xianqu_code.append(21611)
    xianqu_code.append(103)

    def start_requests(self):  # 重写start_requests函数
        start_urls = ['http://{}/xiaoqu/{}/'.format(self.host, code) for code in self.xianqu_code]
        for url in start_urls:
            yield Request(url)  # 遍历所有区域

    def parse(self, response):

        """
        第一步抓取所有的小区
        http://cd.58.com/xiaoqu/21611/
        :param response:
        :return:
        """

        url_list = parse(response)  # 调用utils文件夹中parse文件中的parse方法，得到所有小区的url

        for url in url_list:
            yield Request(url,
                          callback=self.xiaoqu_detail_pag,  # 回调xiaoqu_detail_pag方法
                          errback=self.error_back,
                          priority=4
                          )

    def xiaoqu_detail_pag(self, response):

        """
        第二步抓取小区详情页信息
        http://cd.58.com/xiaoqu/shenxianshudayuan/
        :param response:
        :return:
        """

        _ = self
        data = xiaoqu_parse(response)
        item = City58ItemXiaoQu()
        item.update(data)
        item['id'] = response.url.split('/')[4]
        yield item

        # 二手房
        url = 'http://{}/xiaoqu/{}/ershoufang/'.format(self.host, item['id'])
        yield Request(url,
                      callback=self.ershoufang_list_pag,  # 回调ershoufang_list_pag方法
                      errback=self.error_back,
                      meta={'id': item['id']},
                      priority=3)

        # 出租房
        url_ = 'http://{}/xiaoqu/{}/chuzu/'.format(self.host, item['id'])

        yield Request(url_,
                      callback=self.chuzu_list_pag,  # 回调chuzu_list_pag方法
                      errback=self.error_back,
                      meta={'id': item['id']},
                      priority=2)

    def ershoufang_list_pag(self, response):

        """
        第三步抓取二手房详情页信息
        http://cd.58.com/xiaoqu/shenxianshudayuan/ershoufang/
        :param response:
        :return:
        """

        _ = self
        price_list = get_ershou_price_list(response)

        yield {'id': response.meta['id'], 'price_list': price_list}

    def chuzu_list_pag(self, response):

        """
        第四步抓取出租房详情页url
        http://cd.58.com/xiaoqu/shenxianshudayuan/chuzu/
        :param response:
        :return:
        """

        _ = self
        url_list = chuzu_list_pag_get_detail_url(response)

        for url in url_list:
            yield response.request.replace(url=url, callback=self.chuzu_detail_pag, priority=1)  # 回调chuzu_detail_pag方法
            # yield Request(url, callback=)

    def chuzu_detail_pag(self, response):

        """
        第五步抓取出租房详情页信息
        :param response:
        :return:
        """

        _ = self
        data = get_chuzu_house_info(response)
        item = City58ItemXiaoChuZuQuInfo()
        item.update(data)
        item['id'] = response.meta['id']
        item['url'] = response.url
        yield item

    def error_back(self, e):
        _ = e
        self.logger.error(format_exc())
