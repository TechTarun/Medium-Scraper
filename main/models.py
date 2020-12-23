from django.db import models

# Create your models here.
class Blog(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=500, default="")
    author = models.CharField(max_length=100, default="")
    link = models.CharField(max_length=500)
    num_of_responses = models.IntegerField(default=0)
    date_of_scraping = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.TextField(null=True)

    def __str__(self):
        return self.blog.title


    