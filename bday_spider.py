# -*- coding: utf-8 -*-
import scrapy

class MessagesSpider(scrapy.Spider):
    name = 'messages'
    allowed_domains = ['what-to-write-in-a-card.com']
    start_urls = ['http://www.what-to-write-in-a-card.com/general-birthday-messages/']

    def parse(self, response):
        for item in response.css('td'):
            msg = item.css('td::text').extract_first()
            msg = format_message(msg)
            if msg:
                bday_messages = {'message': msg}
            yield bday_messages

        # 4. Following Pagination Links with Scrapy (https://www.youtube.com/watch?v=G9Nni6G-iOc)
            # follow pagination link, until there are no more next_page_urls 
        next_page_url = response.css('div#page-links > p > a::attr(href)').extract_first()
        print next_page_url
        if next_page_url: 
            next_page_url = response.urljoin(next_page_url)
            print next_page_url
            yield scrapy.Request(url=next_page_url, callback=self.parse)


def format_message(string):
    return string.replace("\u2019", "").replace("\r", "").replace('\t', "").replace('\n', "").lstrip().rstrip()
