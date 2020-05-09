# -*- coding: utf-8 -*-
import scrapy
from tarea1_scrapy.items import articles,article
from w3lib.html import remove_tags


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['en.wikipedia.com']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']

    def parse(self, response):
        host = self.allowed_domains[0]

        for link in response.css(".featured_article_metadata > a"):
            followLink = f"https://{host}{link.attrib.get('href')}"
            link = f"{link.attrib.get('href')}"
            title = link
            yield response.follow(followLink,callback=self.parse_detail,meta={'link':followLink,'title':title})


    def parse_detail(self,response):
        items = articles()
        item = article()

        items["link"] = response.meta["link"]
        item["title"] = response.css("h1::text").extract()[0]
        #text =  response.css(".mw-parser-output > p").extract()[1]

        for text in response.css(".mw-parser-output > p").extract():
            if('mw-empty-elt' in str(text)):
                print("entro")
                continue
            else:
                item["paragraph"] = remove_tags(text)
                break
        
            
        items["body"] = item
        return items
