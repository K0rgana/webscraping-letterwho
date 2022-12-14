import scrapy
import logging
import re
from datetime import datetime

u_base = 'https://www.bigfinish.com'
u_range= 'ranges/v/torchwood'
u_page = "/page:{}"
#urlPage = 'https://www.bigfinish.com/ranges/v/torchwood/page:{}?url=ranges/v/torchwood&sort_ordering=date_asc'
urlPage = 'https://www.bigfinish.com/ranges/v/torchwood/page:{}'

url = f"{u_base}{u_range}{u_page.format(1)}"

class BfSpider(scrapy.Spider):
    name = 'bf_stories'
    start_urls = [urlPage.format(1)]
    #start_urls = [u_base]


    def parse(self, response):
        #get link from items list
        for itn in response.css('.item.release-items'):
            url_item = itn.css('.item.release-items .title a::attr(href)').get()
            url_deep = f"{u_base}{url_item}"
            #url_deep = 'https://www.bigfinish.com/releases/v/doctor-who-shadow-of-the-daleks-1-2051'
            
            #collect data from each item from list
            yield scrapy.Request(url_deep,callback=self.parse_st)

            """ yield {
                'title' : itn.css('.item.release-items .title a::text').get().strip(),
                'url' : urlI,
                'range' : itn.css('.item.release-items .name a::text').get().strip(),
            } """

            #go to next page
            next_pg = response.css('#pagination a').attrib['href']
            if next_pg:
                    abs_url = f"{u_base}{next_pg}"
                    yield scrapy.Request(url=abs_url,callback=self.parse)
            else:
                msg ='No Page Left'
                self.log(msg,logging.WARNING)
                pass

    def parse_st(self, response):
        for st in response.css('.detail-page-outer'):
            #clean resealed
            date = st.css('.product-desc .release-date ::text').get().split('\n')
            date = date[2].strip()
            #convert resealed date 
            mon, yer = date.split(' ')            
            mon = datetime.strptime(mon, '%B').month
            date = f"{yer}-{mon}"

            #fix url
            img = st.css('.detail-page-image img::attr(src)').get()
            uri_img = f"{u_base}{img}"


            CLEANR = re.compile('<.*?>') 

            def cleanhtml(raw_html):
                cleantext = re.sub(CLEANR, '', raw_html)
                return cleantext
            
            f_desc = []
            f_cast = []
            f_crew = []

            #clean desc
            desc = st.css('#tab1 article p').getall()
            for ds in desc:
                a = cleanhtml(ds).strip()
                f_desc.append(a)
            
            newlist = "\n"
            desc = newlist.join(f_desc).replace('\u2019', '\'')
            


            #clean duration
            duration = st.xpath('//li[contains( text(), "minute")]/text()').get().strip()
            duration = duration.split(' ')
            duration = duration[0]

            for cast in st.css('#tab5 li'):
                name = cast.css('li a::text').get().strip()
                role = cast.css('li').get().split('\n')
                role = role[3].replace(')', '').replace('(', '').strip()
                cs = {'actor' : name,'role' : role }
                f_cast.append(cs)

            """ for crew in st.css('#tab6'):
                role = crew.xpath('.//li[@class="comma-seperate-links"]/text()').get().strip()
                name = crew.xpath('//div[@id="tab6"]//li[1]/a/@title').getall()
                
                nm = []
                if len(name) > 1:
                    for n in name:
                        c = {'role' : role ,'p' : n}
                        nm.append(c)
                        f_crew.append(nm)
                else:
                    cw = {'role' : role ,'pp' : name}
                    f_crew.append(cw) """
            
            #clear crew
            clear_lines =[]
            all_lines = st.css('#tab6 .comma-seperate-links').getall()
            for line in all_lines:
                line_clear = cleanhtml(line).strip()   
                clear_lines.append(line_clear)

            for line in clear_lines:
                line = line.split('\n')
                role = line[0]
                line.remove(role)

                #pers = []
                if len(line) > 1:
                    for newperson in line:
                        c = {'role' : role ,'person' : newperson}
                        f_crew.append(c)
                else:
                    pers2 = {'role' : role ,'person' : line}
                    f_crew.append(pers2)

            
                
                #self.log(pers,logging.WARNING)
            
            yield {
                    'story': '',
                    'title' : st.css('.product-desc h3::text').get().strip(),
                    'range' : st.css('.product-desc h6 a::text').get().strip(),
                    'doctor': '',
                    'airdate' : date,
                    'runtime' : duration,

                    'resume' : {'en':desc, 'pt':''},
                    'cast' : f_cast,
                    'crew' : f_crew,
                    'quotes': [{'en':'', 'pt':''},],
                    'cover' : uri_img,
                    'url' : response.url,
                }