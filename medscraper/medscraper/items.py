import scrapy


class MedscraperLinkItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    responses = scrapy.Field()

class MedscraperBlogItem(scrapy.Item):
    id = scrapy.Field()
    content = scrapy.Field()
