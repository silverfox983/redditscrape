from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
from reddit.items import RedditItem
from scrapy.exceptions import DontCloseSpider
import time
import json
import base64
import requests




class RedditSpider(CrawlSpider):
    name = 'reddit'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/RoastMe/.json?limit=1',]

    def parse(self, response):
        data = json.loads(response.body)
        # deal with next page
        if data['data']['after']:
            nextlinx = "https://www.reddit.com/r/RoastMe/.json?limit=1"  + "&after=" + data['data']['after'] + "&count=1" + ".json?limit=1"
            yield response.follow(nextlinx, self.parse_author)
            
            

    

    def parse_author(self, response):
        data = json.loads(response.body)
        nextlink = "https://www.reddit.com/" + data['data']['children'][0]['data']['permalink'] + "&sort=top.json"
        yield response.follow(nextlink, self.parse_page)


    def parse_page(self, response):
        author = json.loads(response.body)
        nextlinker = "https://www.reddit.com/r/RoastMe/.json?limit=1"  + "&after=" + author[0]['data']['children'][0]['data']['name'] + "&count=1" + ".json?limit=1" 
        items = RedditItem()
        
        try:
            items['insult'] = author[1]['data']['children'][0]['data']['body']
            #items['picture'] = base64.b64encode(requests.get(author[0]['data']['children'][0]['data']['url']).content).decode('ascii'),
            items['picture'] = author[0]['data']['children'][0]['data']['url'],
            yield items
            yield response.follow(nextlinker, self.parse)
        except:
            items['insult'] = 'null'
            yield response.follow(nextlinker, self.parse)
            DontCloseSpider
            pass
    
        
        
        # items['picture'] = img_base64duh
        # items['insult'] = author[1]['data']['children'][0]['data']['body']
        
        try:
            yield response.follow(nextlinker, self.parse)
        except:
            print("how is there no more links?")
    