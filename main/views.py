from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def crawl(request):
    return JsonResponse({
        "status" : "Crawling Started"
    })

def crawlstatus(request, **kwargs):
    return JsonResponse({
        "status" : "Crawling Done",
        "id" : kwargs["id"]
    })

    