import scrapy
from ..items import MedscraperBlogItem

class BlogSpider(scrapy.Spider):
    name='blog'
    start_urls = []

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.start_urls.append(kwargs["link"])

    def parse(self, response):
        blogitem = MedscraperBlogItem()

        content = ""
        content_data = response.css("p::text").extract()
        for p in content_data:
            if p != 'Written by':
                content += p

        blogitem["id"] = self.id
        blogitem["content"] = content
        
        yield blogitem