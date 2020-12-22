from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    num_of_responses = models.IntegerField()

    