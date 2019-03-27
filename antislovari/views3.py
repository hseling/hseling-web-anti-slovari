from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render
from antislovari.models import Post
import requests


API_LINK = 'http://127.0.0.1:80'


def home(request):
    if request.method == "POST":
        header = {"Content-type": "application/json"}
        r = requests.post('{}/query'.format(API_LINK), json=request.POST, headers=header)
        # print('RETURN IS ', r.text)
        string_to_return = r.text
        file_to_send = ContentFile(string_to_return)
        response = HttpResponse(file_to_send,'application/x-gzip')
        response['Content-Length'] = file_to_send.size
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(request.POST.get("file", ""))
        return response
    return render(request, 'index.html', {})

def news(request):
    blog_posts = Post.objects.all()
    return render(request, 'news.html', {'blog_posts': blog_posts})

def about(request):
    return render(request, 'about.html', {})

def download(request):
    if request.method == "POST":
        header = {"Content-type": "application/json"}
        print(request.POST.get("file", ""))
        r = requests.post("{}/load_file".format(API_LINK), headers=header, \
            json={'file': request.POST.get("file", "")})
        string_to_return = r.text
        file_to_send = ContentFile(string_to_return)
        response = HttpResponse(file_to_send,'application/x-gzip')
        response['Content-Length'] = file_to_send.size
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(request.POST.get("file", ""))
        return response
    r = requests.get('{}/files'.format(API_LINK))
    files = r.json()['file_ids']
    return render(request, 'download.html', {'files': files})

def links(request):
    return render(request, 'links.html', {})

def stats(request):
    return render(request, 'stats.html', {})
