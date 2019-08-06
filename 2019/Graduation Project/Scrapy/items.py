import scrapy

class SearchtutorialItem(scrapy.Item):
    keyword = scrapy.Field()
    prev_url = scrapy.Field()
    curr_url = scrapy.Field()
    contents = scrapy.Field()
