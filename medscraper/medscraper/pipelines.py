from itemadapter import ItemAdapter
from main.models import Blog, BlogPost
from datetime import datetime as dt

class MedscraperLinkPipeline:
    def __init__(self, unique_id, *args, **kwargs):
        self.items = []
        self.unique_id = unique_id

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'),
        )

    def close_spider(self, spider):
        for item in self.items:
            blog = Blog()
            blog.unique_id = self.unique_id
            blog.date_of_scraping = dt.today().strftime("%d-%m-%Y")
            blog.title = item['title']
            blog.author = item['author']
            blog.num_of_responses = item['responses']
            blog.link = item['link']
            blog.save()

    def process_item(self, item, spider):
        if spider.name == 'bloglink':

            if len(item["title"]) != 0 and len(item["link"]) != 0 and len(item["author"]) != 0:
                blogtitle = item["title"][0]
                blogauthor = item["author"][0]
                if len(item["responses"]) == 0:
                    responses = 0
                else:
                    responses = int(item["responses"][0].split(" ")[0])
                bloglink = item["link"][0]
                self.items.append(
                    {
                        "title" : blogtitle, 
                        "author" : blogauthor, 
                        "responses" : responses, 
                        "link" : bloglink
                    }
                )
            return item

class MedscraperBlogPipeline:

    def saveblog(self, id, content):
        post = BlogPost()
        post.blog = Blog.objects.get(id=id)
        post.content = content
        post.save()

    def process_item(self, item, spider):
        if spider.name == 'blog':
            print("Content = ",len(item["content"]))
            self.saveblog(item["id"], item["content"])
        return item
