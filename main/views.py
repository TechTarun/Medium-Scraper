from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from scrapyd_api import ScrapydAPI
from .models import Blog
import time
from uuid import uuid4

scrapyd = ScrapydAPI('http://localhost:6800')

@csrf_exempt
@require_POST
def crawlLinks(request):
    tag = request.POST.get("tag")
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
        # time.sleep(1)

    return JsonResponse({
        "status" : "Crawling Links Done",
        "task_id" : job_id,
        "unique_id" : unique_id
    })

@csrf_exempt
@require_POST
def crawlBlogs(request):
    unique_id = request.POST.get("unique_id")
    print(unique_id)
    links = list(Blog.objects.filter(unique_id=unique_id))
    blog_job_data = list()

    for link in links:
        job_id = scrapyd.schedule('default', 'blog', id=link.id, link=link.link)
        blog_job_data.append(job_id)

    jobs_done = 0
    while(jobs_done < len(blog_job_data)):
        jobs_done = 0
        print("-----------STATUS OF JOBS--------------")
        for job_id in blog_job_data:
            status = scrapyd.job_status('default', job_id)
            print(status)
            if status == 'finished':
                jobs_done += 1
        time.sleep(2)


    return JsonResponse({
        "status" : "Crawling Done",
        "data" : blog_job_data
    })

@csrf_exempt
def crawlstatus(request, **kwargs):
    task_id = kwargs["task_id"]
    status = scrapyd.job_status('default', task_id)
    return JsonResponse({
        "status" : status
    })

    