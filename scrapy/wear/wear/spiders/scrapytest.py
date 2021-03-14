import scrapy

class wearSpider(scrapy.Spider):
    name = 'wear'
    start_urls = ['https://wear.tw/men-ranking/user/']

    def parse(self, response):
        # for href in response.css('p.item-user-header-avatar > a ::attr(href)'):
        #     userUrl = response.urljoin(href.extract())
        #     print(url)
        for post in response.css('li.first-line-item'):
            yield {
                'rank' : post.css('p::text')[0].get(),
                'userUrl' : post.css('p.item-user-header-avatar > a::attr(href)').get()
            }
            
            # print(dict(rank=rank,userUrl=userUrl))

        # yield scrapy.Request(url, callback=self.parse_post)
        # filename = response.url.split('/')[-1] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)