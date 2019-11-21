# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from urllib import parse
from Jobbole.items import JobboleItem


class JobboleSpider(RedisSpider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    reids_key = 'jobbole:start_urls'


    def parse(self, response):

        """
        逻辑分析
            1.通过抓取下一页的链接，交给scrapy实现自动翻页,如果没有下一页则爬取完成
            2.将本页面的所有文章url爬下，并交给scrapy进行深入详情页的爬取
        """
        node_urls = response.css('#archive .floated-thumb .post-thumb a')
        for node_url in node_urls:
            title_url = node_url.css('::attr(href)').extract_first("")
            title_img = node_url.css('img::attr(src)').extract_first("")

            yield Request(url=parse.urljoin(response.url, title_url), meta={"title_img": title_img},
                          callback=self.parse_detail)

        # 实现下一页的翻页爬取
        next_pages = response.css('.next.page-numbers::attr(href)').extract_first("")  # 在当前列表页获取下一页链接
        if next_pages:
            yield Request(url=parse.urljoin(response.url, next_pages),
                          callback=self.parse)  # 如果存在下一页，则将下一页交给parse自身处理

    def parse_detail(self, response):
        """
        将爬虫爬取的数据送到item中进行序列化
        这里通过ItemLoader加载item
        """
        item = JobboleItem()
        item['title_image'] = response.meta.get('title_img')
        yield item
