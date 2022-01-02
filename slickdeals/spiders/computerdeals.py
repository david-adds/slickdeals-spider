import scrapy
from scrapy_selenium import SeleniumRequest


class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'
    
    def start_request(self):
        yield SeleniumRequest(
            url="https://slickdeals.net/computer-deals/",
            wait_time=3,
            callback = self.parse
        )
        
    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals blueprint']/li") #[contains(@class,'fpGridBox grid')]")
        for product in products:
            # try:
            yield{
                "name": product.xpath(".//a[contains(@class,'itemTitle bp-p-deal')]/text()").get(),
                "link": product.xpath(".//a[contains(@class,'itemTitle bp-p-deal')]/@href").get(),
                "store_name": product.xpath(".//button[contains(@class,'itemStore')]/text() | //a[contains(@class,'itemStore bp-p-store')]/text()").get(),
                "price": product.xpath(".//div[contains(@class,'itemPrice')]/text()").get()
            }
        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )
                