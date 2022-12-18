import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import re
from datetime import datetime

ranges_hub = {
    '1':'ranges/v/torchwood',
    '2':'ranges/v/torchwood-special-releases',
    '3': 'ranges/v/torchwood-the-story-continues',
    '4': 'ranges/v/torchwood-one',
    '5': 'ranges/v/torchwood-soho',
    '6': 'ranges/v/unit',
    '7': 'ranges/v/unit---the-new-series',
    '8': 'ranges/v/the-worlds-of-doctor-who---special-releases',
    '9': 'ranges/v/doctor-who-the-new-adventures-of-bernice-summerfield',
    '10': 'ranges/v/bernice-summerfield',
    '11': 'ranges/v/bernice-summerfield-books',
    '12': 'ranges/v/charlotte-pollard',
    '13': 'ranges/v/iris-wildthyme',
    '14': 'ranges/v/iris-wildthyme-and-friends',
    '15': 'ranges/v/river-song',
    '16': 'ranges/v/sarah-jane-smith',
    '17': 'ranges/v/the-lives-of-captain-jack',
    '18': 'ranges/v/jago-litefoot',
    '19': 'ranges/v/the-paternoster-gang',
    '20': 'ranges/v/counter-measures',
    '21': 'ranges/v/class',
    '22': 'ranges/v/the-robots',
    '23': 'ranges/v/missy',
    '24': 'ranges/v/the-war-master',
    '25': 'ranges/v/gallifrey',
    '26': 'ranges/v/cyberman',
    '27': 'ranges/v/dalek-empire',
    '28': 'ranges/v/i-davros',
    '29': 'ranges/v/doctor-who---the-first-doctor-adventures',
    '30': 'ranges/v/doctor-who-the-second-doctor-adventures',
    '31': 'ranges/v/doctor-who---the-third-doctor-adventures',
    '32': 'ranges/v/doctor-who---fourth-doctor-adventures',
    '33': 'ranges/v/doctor-who---the-fifth-doctor-adventures',
    '34': 'ranges/v/doctor-who---the-sixth-doctor-adventures',
    '35': 'ranges/v/doctor-who---the-seventh-doctor-adventures',
    '36': 'ranges/v/eighth-doctor-adventures',
    '37': 'ranges/v/doctor-who---the-war-doctor',
    '38': 'ranges/v/doctor-who-the-ninth-doctor-adventures',
    '39': 'ranges/v/doctor-who---the-tenth-doctor-adventures',
    '40': 'ranges/v/monthly-series',
    '41': 'ranges/v/doctor-who-the-audio-novels',
    '42': 'ranges/v/doctor-who---companion-chronicles',
    '43': 'ranges/v/doctor-who---the-early-adventures1',
    '44': 'ranges/v/doctor-who---the-lost-stories',
    '45': 'ranges/v/doctor-who---short-trips',
    '46': 'ranges/v/doctor-who---short-trips-rareties',
    '47': 'ranges/v/doctor-who---the-doctor-chronicles',
    '48': 'ranges/v/doctor-who---unbound',
    '49': 'ranges/v/doctor-who-time-lord-victorious',
    '50': 'ranges/v/doctor-who-once-and-future',
    '51': 'ranges/v/doctor-who-destiny-of-the-doctors',
    '52': 'ranges/v/doctor-who---novel-adaptations',
    '53': 'ranges/v/doctor-who---classic-series---special-releases',
    '54': 'ranges/v/doctor-who-philip-hinchcliffe-presents',
    '55': 'ranges/v/doctor-who-auf-deutsch',
    '56': 'ranges/v/doctor-who---the-stage-plays',
}

# See who the url is divided:
#              |           base         |      range       | page |           filters
#urlExemple = 'https://www.bigfinish.com/ranges/v/torchwood/page:{}?url=ranges/v/torchwood&sort_ordering=date_asc'

#PASTE INSIDE THE ' ' AND AFTER THE "/v/" THE RANGE NAME/URL FROM BIG FINISH SITE
#u_range = 'ranges/v/torchwood'
u_range = ranges_hub["1"]
u_page = "/page:{}"
u_base = 'https://www.bigfinish.com'
u_filter_asc = f"?url={u_range}&sort_ordering=date_asc"
u_filter_des = f"?url={u_range}&sort_ordering=date_des"
url = f"{u_base}/{u_range}{u_page.format(1)}{u_filter_asc}"

rg = u_range.split('/')
rg = rg[2]

class BfStoriesSpider(scrapy.Spider):
    name = 'bf_stories'
    start_urls = [url]

    def parse(self, response):
        #get link from items list
        for itn in response.css('.item.release-items'):
            url_item = itn.css('.item.release-items .title a::attr(href)').get()
            url_deep = f"{u_base}{url_item}"
            #url_deep = 'https://www.bigfinish.com/releases/v/doctor-who-the-war-doctor-only-the-monstrous-1380'
            
            #collect data from each item from list
            yield scrapy.Request(url_deep,callback=self.parse_st)

            #go to next page
            next_pg = response.css('#pagination a').attrib['href']
            if next_pg:
                    abs_url = f"{u_base}{next_pg}"
                    yield scrapy.Request(url=abs_url,callback=self.parse)
            
            #read the last page
            last_url = f"{u_base}/{u_range}{u_page.format(1)}{u_filter_des}"
            yield scrapy.Request(url=last_url,callback=self.parse)

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
            
            #trailer url
            trailer = st.css('#tab4 iframe::attr(src)').get()

            CLEANR = re.compile('<.*?>') 

            def cleanhtml(raw_html):
                cleantext = re.sub(CLEANR, '', raw_html)
                return cleantext
            
            f_desc = []
            f_cast = []
            f_crew = []

            #clean title and story
            title_full = st.css('.product-desc h3::text').get().strip()
            nw_ttl = re.split('\.\s',title_full)
            story = nw_ttl[0]
            title = nw_ttl[1]

            #clean desc
            desc = st.css('#tab1 article p').getall()
            for ds in desc:
                a = cleanhtml(ds).strip()
                f_desc.append(a)
            newlist = "\n"
            desc = newlist.join(f_desc).replace('\u2019', '\'').replace('\u2026', '...')
            
            #clean duration
            duration = st.xpath('//li[contains( text(), "minute")]/text()').get().strip()
            duration = duration.split(' ')
            duration = duration[0]

            range = st.css('.product-desc h6 a::text').get().strip() 
            ISBNP = st.xpath('//*[@id="tab6"]/div/div[2]/ul/li[4]/text()').get().strip()
            ISBND = st.xpath('//*[@id="tab6"]/div/div[2]/ul/li[5]/text()').get().strip()
            codeProd = st.xpath('//*[@id="tab6"]/div/div[2]/ul/li[6]/text()').get().strip()

            #clear cast
            for cast in st.css('#tab5 li'):
                name = cast.css('li a::text').get().strip()
                role = cast.css('li').get().split('\n')
                role = role[3].replace(')', '').replace('(', '').strip()
                cs = {'actor' : name,'role' : role }
                f_cast.append(cs)
            
            #clear crew
            clear_lines =[]
            all_lines = st.css('#tab6 .comma-seperate-links').getall()
            for line in all_lines:
                line_clear = cleanhtml(line).strip()   
                clear_lines.append(line_clear)

            for line in clear_lines:
                line =line.replace('\t', '')
                line = line.split('\n')
                role = line[0]
                line.remove(role)

                if len(line) > 1:
                    for newperson in line:
                        c = {'role' : role ,'person' : newperson}
                        f_crew.append(c)
                else:
                    pers2 = {'role' : role ,'person' : line[0]}
                    f_crew.append(pers2)

            yield {
                    'contribution': 'korgana',
                    'story': story,
                    'title' : title,
                    'range' : range,
                    'doctor': '',
                    'airdate' : date,
                    'runtime' : duration,
                    'resume' : {'en':desc, 'pt':''},
                    'cast' : f_cast,
                    'crew' : f_crew,
                    'quotes': [{'en':'', 'pt':''},],
                    'Physical Retail ISBN' : ISBNP,
                    'Digital Retail ISBN' : ISBND,
                    'Production Code' : codeProd,
                    'cover' : uri_img,
                    'trailer' : trailer,
                    'url' : response.url,
                }

#run the script and make json file
output = f"output-{rg}.csv"
process = CrawlerProcess(settings={
    "FEED_URI": output,
    "FEED_FORMAT": "csv"
})
process.crawl(BfStoriesSpider)
process.start() # the script will block here until the crawling is finished