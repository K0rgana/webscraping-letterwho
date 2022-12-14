import scrapy

baseUrl = 'https://www.bigfinish.com'
urlPage = 'https://www.bigfinish.com/ranges/v/monthly-series/page:{}'


class BfSpider(scrapy.Spider):
    name = 'bf'
    start_urls = [urlPage.format(1)]
    #start_urls = ['https://www.bigfinish.com/ranges/v/monthly-series/page:36']

    def parse(self, response):
        for itn in response.css('.item.release-items'):
            urlItem = itn.css('.item.release-items .title a::attr(href)').get()
            urlI = f"{baseUrl}{urlItem}"

            yield {
                'title' : itn.css('.item.release-items .title a::text').get().strip(),
                'url' : urlI,
                'range' : itn.css('.item.release-items .name a::text').get().strip(),
            }

            next_pg = response.css('#pagination a').attrib['href']
            if next_pg:
                    abs_url = f"https://www.bigfinish.com{next_pg}"
                    yield scrapy.Request(url=abs_url,callback=self.parse)
            else:
                print('No Page Left')