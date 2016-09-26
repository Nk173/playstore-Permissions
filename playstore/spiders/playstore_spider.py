# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from playstore.items import PlaystoreItem
from scrapy.http import Request
from scrapy.selector import Selector
import urlparse

class PlaystoreSpiderSpider(scrapy.Spider):
    name = "playstore_spider"
    allowed_domains = ["play.google.com"]
    start_urls = (
        'https://play.google.com/store/apps/category/FINANCE',
    )

    def parse(self, response):
        links = response.xpath('//a[@class="title"]/@href').extract()
        for url in links:
            yield scrapy.Request(urlparse.urljoin('https://play.google.com', url[1:]), callback=self.parse_app)

    def parse_app(self, response):
        for app in response.xpath('/html'):
            item=PlaystoreItem()
            item['Name'] = app.xpath('*//div[@class="id-app-title"]//text()').extract()
            item['Downloads'] =app.xpath('*//div[@itemprop="numDownloads"]//text()').extract()

            yield item
