import scrapy

from scrapy.loader import ItemLoader
from ..items import SberbankrsItem
from itemloaders.processors import TakeFirst


class SberbankrsSpider(scrapy.Spider):
	name = 'sberbankrs'
	start_urls = ['https://www.sberbank.rs/o-nama/press-centar']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class, "accordion")]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "news", " " ))]//text()[normalize-space() and not(ancestor::h2 | ancestor::p[@class="date"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "date", " " ))]/text()').get()

		item = ItemLoader(item=SberbankrsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
