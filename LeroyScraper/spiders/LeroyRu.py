import uuid

import bson
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from LeroyScraper.items import LeroyscraperItem


class LeroyruSpider(scrapy.Spider):
    name = 'LeroyRu'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://barnaul.leroymerlin.ru/search/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@data-qa-product]/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyscraperItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('_id', bson.Binary.from_uuid(uuid.uuid3(uuid.NAMESPACE_URL, response.url)))
        loader.add_xpath('name', '//h1//text()')
        loader.add_xpath('price', '//span[@slot="price"]//text()')
        loader.add_xpath('photos', '//img[@slot="thumbs"]/@src')
        loader.add_xpath('characteristics', '//section[@id="characteristics"]//dl/div//text()')
        yield loader.load_item()
