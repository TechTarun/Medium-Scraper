import scrapy
from ..items import MedscraperItem

class MediumScraper(scrapy.Spider):
    name="medium"
    base_url = "https://medium.com/search?q="
    start_urls = []

    def __init__(self):
        self.take_tag_from_user()

    def take_tag_from_user(self):
        tag = input("Enter tag you want to search blogs on = ")
        self.start_urls.append(self.base_url + tag)

    def parse(self, response):
        item = MedscraperItem()
        blogs = response.css("div.postArticle")

        for blog in blogs:
            title = blog.css("h3.graf--title::text").extract()
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