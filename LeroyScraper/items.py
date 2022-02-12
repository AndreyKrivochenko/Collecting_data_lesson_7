# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose


def clean_price(value):
    value = value.replace('\xa0', '')
    try:
        value = int(value)
    except:
        return value
    return value


def replace_size_image(value: str):
    value = value.replace('h_82', 'h_2000').replace('w_82', 'w_2000')
    return value


def get_characteristics(charact: list):
    charact_dict = {}
    for i, value in enumerate(charact):
        if not i % 2:
            charact_dict[charact[i]] = charact[i + 1]
    return charact_dict


class LeroyscraperItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(replace_size_image))
    characteristics = scrapy.Field(input_processor=Compose(get_characteristics), output_processor=TakeFirst())
