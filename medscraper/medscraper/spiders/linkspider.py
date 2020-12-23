import scrapy
from ..items import MedscraperLinkItem

class MediumScraper(scrapy.Spider):
    name="bloglink"
    base_url = "https://medium.com/search?q="
    start_urls = []

    def __init__(self, **kwargs):
        tag = kwargs['tag']
        self.start_urls.append(self.base_url + tag)

    def parse(self, response):
        item = MedscraperLinkItem()
        blogs = response.css("div.postArticle")

        for blog in blogs:
            title = blog.css("h3.graf--title::text").extract()
            if len(title) == 0:
                title = blog.css(".graf--title strong::text").extract()
            author = blog.css("div.ui-captionStrong a.link::text").extract()
            link = blog.css("div.postArticle-readMore a.button::attr(href)").extract()
            responses = blog.css("div.u-floatRight a::text").extract()

            item["title"] = title
            item["author"] = author
            item["link"] = link
            item["responses"] = responses
            yield item

"""
Selectors : 
    1- Author Name : response.css("div.ui-captionStrong a.link::text").extract()
    2- Blog Name : response.css("h3.graf--title::text").extract()
    3- Responses : response.css("div.u-floatRight a::text").extract()
    4- Blog Link : response.css("div.postArticle-readMore a.button::attr(href)").extract()
"""