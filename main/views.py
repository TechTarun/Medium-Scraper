from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from scrapyd_api import ScrapydAPI
from .models import Blog
import time
from uuid import uuid4

scrapyd = ScrapydAPI('http://localhost:6800')

class crawlLinks(APIView):
    def post(self, request):
        print(request.data)
        tag = request.data.get("tag")
        print("Tag = ", tag)
        unique_id = str(uuid4())
        job_id = scrapyd.schedule(
            'default', # Project
            'bloglink',  # Spider
            settings={
                "unique_id" : unique_id
            },
            tag=tag
        )

        status = scrapyd.job_status('default', job_id)
        while(status != "finished"):
            status = scrapyd.job_status('default', job_id)
            print(status)
            time.sleep(1)

        return Response({
            "status" : HTTP_200_OK,
            "message" : "Crawling Links Done",
            "task_id" : job_id,
            "unique_id" : unique_id
        })

class crawlBlogs(APIView):
    def post(self, request):
        unique_id = request.data.get("unique_id")
        print(unique_id)
        links = list(Blog.objects.filter(unique_id=unique_id))
        blog_job_data = list()

        for link in links:
            job_id = scrapyd.schedule('default', 'blog', id=link.id, link=link.link)
            link.unique_id = job_id
            link.save()
            blog_job_data.append(job_id)
        print(blog_job_data)

        # jobs_done = 0
        # while(jobs_done < len(blog_job_data)):
        #     jobs_done = 0
        #     print("-----------STATUS OF JOBS--------------")
        #     for job_id in blog_job_data:
        #         status = scrapyd.job_status('default', job_id)
        #         print(status)
        #         if status == 'finished':
        #             jobs_done += 1
        #     time.sleep(2)


        return Response({
            "status" : HTTP_200_OK,
            "message" : "Crawling Blogs...",
            "jobs" : blog_job_data
        })

class crawlstatus(APIView):
    def post(self, request):
        task_id = request.data.get("job_id")
        print(task_id)
        output_status = list()
        for job_id in task_id:
            status = scrapyd.job_status('default', job_id)
            if status == "finished":
                blog = Blog.objects.get(unique_id=job_id)
                output_status.append([blog.title, blog.author, blog.num_of_responses])
            else:
                output_status.append(status)
        return Response({
            "status" : HTTP_200_OK,
            "message" : output_status
        })

    