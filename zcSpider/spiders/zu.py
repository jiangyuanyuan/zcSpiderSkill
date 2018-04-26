# -*- coding: utf-8 -*-
import scrapy

from zcSpider.items import ZcspiderItem


class DongdongSpider(scrapy.Spider):
    name = 'zu'
    allowed_domains = ['www.dacai.com']
    # http: // www.dacai.com / news / bd / zjyc / list4.html
    url = 'http://www.dacai.com/news/zc/jq/'
    offset = 1
    start_urls = [url]


    def parse(self, response):
        # 每一页里的所有帖子的链接集合
        links = response.xpath('//div[@class="tbgz"]//li//a/@href').extract()

        # 迭代取出集合里的链接
        for link in links:
            if link != '':
                # 提取列表里每个帖子的链接，发送请求放到请求队列里,并调用self.parse_item来处理
                # print link
                yield scrapy.Request(link, callback = self.parse_item)


        # 页面终止条件成立前，会一直自增offset的值，并发送新的页面请求，调用parse方法处理
        # if self.offset <= 35:
        #     self.offset += 1
        #     # 发送请求放到请求队列里，调用self.parse处理response
        #     yield scrapy.Request("http://www.dacai.com/news/bd/zjyc/list" +str(self.offset)+".html", callback = self.parse)

    # 处理每个帖子的response内容
    def parse_item(self, response):
        item = ZcspiderItem()
        # 标题
        # item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0]
        item['title'] = response.xpath('//div[@class="z_left"]//h1/text()').extract()[0]
        # 时间
        item['time'] = response.xpath('//div[@class="z_left"]//div[@class="newstitle"]//p/text()').extract()[0]
        # 内容，先使用有图片情况下的匹配规则，如果有内容，返回所有内容的列表集合
        contents = response.xpath('//div[@class="z_left"]//div[@class="text"]//span/text()').extract()
        contents1 = response.xpath('//div[@class="z_left"]//div[@class="text"]//span//strong/text()').extract()
        content =""
        for cont in contents1:
            content = content+cont
        for cont in contents:
            content = content+cont
        item['content']= content
        # print content
        item['url'] = response.url

        # 交给管道
        yield item

