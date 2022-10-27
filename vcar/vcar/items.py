# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VcarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    car_id = scrapy.Field()
    company_id = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    full_name = scrapy.Field()
    car_name = scrapy.Field()
    segment_name = scrapy.Field()
    segment_company = scrapy.Field()
    version_id = scrapy.Field()
    price = scrapy.Field()
    tskt_version = scrapy.Field()
    list_version = scrapy.Field()
    thumbnail_url = scrapy.Field()
    arrImages = scrapy.Field()
