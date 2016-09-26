# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from playstore.items import PlaystoreItem
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import urlparse

class PlaystoreSpiderSpider(scrapy.Spider):
    name = "selenium_spider"
    allowed_domains = ["play.google.com"]
    start_urls = (
        'https://play.google.com/store/apps/category/FINANCE/collection/topselling_free?hl=en',
    )
    def __init__(self):
        self.driver = webdriver.Chrome('C:/Python27/selenium/webdriver/chromedriver.exe')

    def parse(self, response):
        self.driver.get(response.url)
        copyright = self.driver.find_element_by_class_name('copyright')
        showmore = self.driver.find_element_by_id('show-more-button')
        ActionChains(self.driver).move_to_element(copyright).perform()
        ActionChains(self.driver).move_to_element(showmore).perform()

        # To scroll the page till the show more button appears
        while not showmore.is_displayed():
            copyright = self.driver.find_element_by_class_name('copyright')
            time.sleep(2) #to let page content loading
            ActionChains(self.driver).move_to_element(copyright).perform()

        showmore.click()
        # To scroll down till the we see the copyright which marks the end of the page
        while not copyright.is_displayed():
            copyright = self.driver.find_element_by_class_name('copyright')
            time.sleep(2) #to let page content loading
            ActionChains(self.driver).move_to_element(copyright).perform()

        time.sleep(5) # To let page content load
        # To identify all partial urls of every app displayed
        # links = response.xpath('//a[@class="title"]/@href').extract()
        links = self.driver.find_elements_by_xpath('*//a[@class="title"]')
        # print(len(links))
        # i=0;

        # getting the complete url and pushing a request
        for url in links:
            # print(urlparse.urljoin('https://play.google.com', url.get_attribute("href")))
            # i = i+1;
            yield scrapy.Request(urlparse.urljoin('https://play.google.com', url.get_attribute("href")), callback=self.parse_app, dont_filter = True)
            # print(len(links)-i)

    def parse_app(self, response):
        # Opening a second browser instance to avoid confusion
        driver2 = webdriver.Chrome('C:/Python27/selenium/webdriver/chromedriver.exe')
        driver2.get(response.url)

        time.sleep(5) # To let page content load

        for app in response.xpath('/html'):
            item=PlaystoreItem()
            item['Name'] = app.xpath('*//div[@class="id-app-title"]//text()').extract()
            item['Developer'] = app.xpath('//span[@itemprop="name"]//text()').extract()
            item['Downloads'] =app.xpath('*//div[@itemprop="numDownloads"]/text()').extract()
            item['LastUpdate'] = app.xpath('*//div[@itemprop="datePublished"]/text()').extract()
            item['Size']= app.xpath('*//div[@itemprop="fileSize"]/text()').extract()
            item['Version']= app.xpath('*//div[@itemprop="softwareVersion"]/text()').extract()
            item['andriodRequirements']=app.xpath('*//div[@itemprop="operatingSystems"]/text()').extract()
            item['DeveloperLink']= app.xpath('*//a[@class="dev-link"]/@href').extract()
            item['Rating']= app.xpath('*//div[@class="score"]/text()').extract()
            item['ratingCount'] = app.xpath('*//span[@class ="reviews-num"]/text()').extract()

            # readmore = self.driver.find_element_by_class_name('play-button show-more small')
            # while readmore.is_displayed():
            #     readmore.click()
            Des=[]
            Des1 = app.xpath('*//div[@itemprop = "description"]/div/text()').extract()
            Des2 = app.xpath('*//div[@itemprop = "description"]/div/p/text()').extract()
            item['Description']= Des1 + Des2
            # self.driver.find_element_by_xpath('*//button[contains(text(),"View details")]').click()

            # browser to click on "view details" to get the page to show permissions
            driver2.find_element_by_xpath('*//button[contains(text(),"View details")]').click()
            time.sleep(10) # To let page content load
            permissionBucket = driver2.find_elements_by_xpath('*//ul[@class = "bucket-description"]')

            plist=[] # Permissions list
            for permission in permissionBucket:
                p = permission.text
                plist.append(p)

            item['Permissions'] = plist
            yield item
            # driver2.close()

## CMD in working directory
## scrapy crawl selenium_spider -o permissions_app_fin_free.csv -t csv
