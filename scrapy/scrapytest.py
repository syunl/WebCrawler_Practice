import scrapy

class WearSpider(scrapy.Spider):
    name = "wear"
    start_urls = ['https://wear.tw/men-ranking/user/']
    def parse(self, response):
        a = response.css('span.name')
        print(a.text)
        # yield {
        #         'userID': u.css('a::attr("href")').extract_first(),
        #         }
        