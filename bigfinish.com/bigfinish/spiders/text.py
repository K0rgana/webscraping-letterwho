baseUrl = 'https://www.bigfinish.com/'
rangeurl= 'ranges/v/torchwood'
#urlPage = 'https://www.bigfinish.com/ranges/v/torchwood/page:{}?url=ranges/v/torchwood&sort_ordering=date_asc'
urlPage = "/page:{}"
urlorder = "?sort_ordering=date_asc&search_product_type=&search_availability=all"
""" 
https://www.bigfinish.com/ranges/v/torchwood-the-story-continues?sort_ordering=date_asc&search_product_type=&search_availability=all

https://www.bigfinish.com/ranges/v/torchwood-the-story-continues/page:2?url=ranges%2Fv%2Ftorchwood-the-story-continues&sort_ordering=all&search_availability=all&search_release_date=desc&_=1670537282875 """

start_urls = [urlPage.format(1)]

urlI = f"{baseUrl}{rangeurl}{urlPage.format(1)}"

print(urlI)