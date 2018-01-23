# -*- coding: utf-8 -*-
import scrapy
from shuku.items import ShukuItem
import time 

count = 1

class shukuSpider(scrapy.Spider):
    name = "shuku"
    allowed_domains = ["https://www.52shuku.com"]
    dont_filter=True
    meta={'dont_redirect': True}
    start_urls = ['https://www.52shuku.com/wenxue/']
    #map(lambda elem: 'http://http://www.jokeji.cn/list_' + str(elem) + '.htm',range(1,9+1))
    base_url = 'https://www.52shuku.com'
   

    def parse(self, response):
    	sel=scrapy.Selector(response)
    	articles=sel.css('h2 a[href^="/wenxue/"]').css('a[href$=".html"]')
    	for article in articles:
    		articles_url = self.base_url + article.css('a::attr(href)').extract()[0]
    		if(articles_url is not None):
    			yield scrapy.Request(articles_url, meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [302]
                  },
                  callback=self.parsearticle,
                  dont_filter=True)
    	time.sleep(3)
    	next=sel.css('a[href^="/wenxue/"]')
    	for ne in next:
        	if(ne.css("::text").extract()[0] == "下一页"):
          		next_url = self.base_url  + ne.css("::attr(href)").extract()[0]
          		yield scrapy.Request(next_url, meta = {
                      	'dont_redirect': True,
                      	'handle_httpstatus_list': [302]
                  	},
                  	callback=self.parse,
                  	dont_filter=True)

    def parsearticle(self, response):
    	sel=scrapy.Selector(response)
    	title=sel.css('.article-title::text').extract()[0]
    	
    	conts=sel.css('p')
    	content=''
    	for cont in conts:
    		content = content + cont.css("::text").extract()[0]
    	
    	next=sel.css('a[href^="/wenxue/"]')
    	for ne in next:
    		if(ne.css("::text").extract()[0] == "下一页"):
    			articles_url = self.base_url  + ne.css("::attr(href)").extract()[0]
    			yield scrapy.Request(articles_url, meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [302]
                  },
                  callback=self.parsearticle,
                  dont_filter=True)
    	try:    		
    		shuku_item = ShukuItem()
    		shuku_item['content'] = content
    		shuku_item['title'] = title
    		yield shuku_item
    	except Exception as e:
    		print(e)
    	
