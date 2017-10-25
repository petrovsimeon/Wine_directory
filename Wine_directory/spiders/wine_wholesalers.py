# -*- coding: utf-8 -*-
from scrapy import Spider
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep
import random


class WineWholesalersSpider(Spider):
    name = "wine_wholesalers"
    allowed_domains = ["beveragetradenetwork.com"]
    start_urls = ['http://beveragetradenetwork.com/en/digital-directory/wine-wholesaler-4/page-1//']
    custom_settings = {'FEED_FORMAT': 'csv', 'FEED_URI': 'Wine_wholesalers.csv'}

    def start_requests(self):

        # Logging into the website
        self.driver = webdriver.Chrome('C:/Coding/chromedriver')
        sleep(random.randint(1, 5))
        self.driver.get('http://beveragetradenetwork.com/en/users/log-in.htm')
        sleep (random.randint (1, 5))

        # Entering username
        self.driver.find_element_by_id('user').send_keys("conner.nudd@bermar.co.uk")
        sleep (random.randint (1, 5))

        # Entering password
        self.driver.find_element_by_xpath("//div[@id='inlineAJAXLogInForm']/article/form[@id='FrmLoginInLine']/input[@id='password']").send_keys("Ch4mp4gne!")
        sleep (random.randint (1, 5))
        self.driver.find_element_by_xpath("//div[@id='inlineAJAXLogInForm']/article/form[@id='FrmLoginInLine']/input[@type = 'submit']").send_keys(Keys.ENTER)
        sleep (random.randint(1, 5))

        # Going to Digital Directory
        self.driver.get('http://beveragetradenetwork.com/en/digital-directory/wine-wholesaler-4/page-1/')
        sleep(random.randint(1, 5))


        # Getting companies
        sel = Selector(text=self.driver.page_source)
        companies = sel.xpath('//*[@class="txt"]/h1/a/@href').extract()

        for company in companies:
            url = 'http://beveragetradenetwork.com' + company
            yield Request(url, callback=self.parse_item)



        # Pagination
        while True:
            try:
                next_page = self.driver.find_element_by_link_text('NEXT')
                sleep (random.randint (1, 5))
                next_page.send_keys(Keys.ENTER)
                sleep (random.randint (1, 5))
                self.logger.info('Sleeping for 3 seconds')
                next_page.click()


            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                break


    def parse_item(self, response):

        self.driver.get(response.url)
        response = Selector(text=self.driver.page_source)

        name = response.xpath('//div[@class="txt"]/h1/text()').extract()
        country = response.xpath('//div[@class="txt"]/h3/label[text()="Country:"]/following-sibling::text()').extract()
        address = response.xpath('normalize-space(//h4[text()="Address"]/following-sibling::p/text())').extract()
        phonefax = response.xpath('normalize-space(//h4[text()="Phone & Fax"]/following-sibling::p)').extract()
        contact = response.xpath('normalize-space(//h4[text()="Contact Person"]/following-sibling::p/text())').extract()
        title = response.xpath('normalize-space(//h4[text()="Title"]/following-sibling::p/text())').extract()
        email = response.xpath ('normalize-space(//h4[text()="Email"]/following-sibling::p/text())').extract()
        phone = response.xpath ('normalize-space(//h4[text()="Phone"]/following-sibling::p/text())').extract()
        website = response.xpath ('normalize-space(//h4[text()="Website"]/following-sibling::p/a/@href)').extract()
        linkedin = response.xpath ('normalize-space(//h4[text()="LinkedIN"]/following-sibling::p/a/@href)').extract()
        facebook = response.xpath ('normalize-space(//h4[text()="Facebook"]/following-sibling::p/a/@href)').extract()
        twitter = response.xpath ('normalize-space(//h4[text()="Twitter"]/following-sibling::p/a/@href)').extract()
        description = response.xpath('//div[@class="card2 module1"]/div[@class="description"]/div/p/text()').extract()

        yield {'Company Name': name, 'Country': country, 'Address': address,
               'Phone and Fax': phonefax, 'Contact Person': contact, 'Title': title,
               'Email': email,'Phone': phone, 'Website': website, 'Linkedin': linkedin,
               'Facebook': facebook, 'Twitter': twitter, 'Description': description}

        sleep (random.randint(1, 5))

