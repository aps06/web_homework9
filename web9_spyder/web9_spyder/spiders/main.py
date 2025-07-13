import scrapy
from pathlib import Path
from scrapy.crawler import CrawlerProcess

path = Path(__file__)
path_to_web_homework9 = path.parent.parent.parent.parent
DATA_DIR = Path.joinpath(path_to_web_homework9, "web_homework9/data")
PATH_TO_AUTHORS = Path.joinpath(DATA_DIR, "authors.json")
PATH_TO_QUOTES = Path.joinpath(DATA_DIR, "quotes.json")


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": str(PATH_TO_QUOTES)}

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get(),
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


class AutorsSpider(scrapy.Spider):
    name = "autors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": str(PATH_TO_AUTHORS)}

    def parse(self, response):
        for quote in response.xpath("//div[@class='author-details']"):
            yield {
                    "fullname": quote.xpath(
                        "//h3[@class='author-title']/text()"
                        ).get(),
                    "born_date": quote.xpath(
                        "//span[@class='author-born-date']/text()"
                    ).get(),
                    "born_location": quote.xpath(
                        "//span[@class='author-born-location']/text()"
                    ).get(),
                    "description": quote.xpath(
                        "//div[@class='author-description']/text()"
                        ).get(),
                }

        authors_links = response.xpath("//a[text()='(about)']/@href").extract()
        for author_link in authors_links:
            yield scrapy.Request(url=self.start_urls[0] + author_link)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


# run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.crawl(AutorsSpider)
process.start()
