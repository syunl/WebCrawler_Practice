import scrapy

class wearSpider(scrapy.Spider):
    name = 'wear2'
    start_urls = ['https://wear.tw/1228masa/']

    def parse(self, response):
        for userinfo in response.css('li.like_mark'):
            yield {
                'imgUrl' : userinfo.css('div.image > a.over::attr(href)').get(),
                'imgName' : userinfo.css('div.image > a > p> img::attr(data-originalretina)').get()
            }
            next_page = response.css('p.next > a ::attr(href)').get()
            if next_page is not None:
                next_page =response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)