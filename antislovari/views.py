from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render
from antislovari.models import Post
from unidecode import unidecode
import requests


API_LINK = 'http://127.0.0.1:80'


# def home(request):
#     string_to_return = ''
#     if 'string' in request.session:
#         string_to_return = request.session.get('string')
#     if request.method == "POST" and 'string' in request.data:
#         file_to_send = ContentFile(string_to_return)
#         response = HttpResponse(file_to_send,'application/text')
#         response['Content-Length'] = file_to_send.size
#         disp = 'attachment; filename="{}_antislovari.txt"'.format(unidecode(request.POST["string"]))
#         response['Content-Disposition'] = disp
#         return response
#     elif request.method == "POST":
#         header = {"Content-type": "application/json"}
#         r = requests.post('{}/query'.format(API_LINK), json=request.POST, headers=header)
#         print('RETURN IS ', r.text)
#         string_to_return = r.text
#         request.session['string'] = string_to_return
#         return render(request, 'index.html', {'out': string_to_return.split()})
#     return render(request, 'index.html', {'out': string_to_return.split()[:10]})

def home(request):
    string_to_return = ''
    if 'string_to_return' in request.session:
        string_to_return = request.session.get('string_to_return')
    if request.method == "POST" and 'download_button' in request.POST:
        print("TO RETURN", string_to_return)
        file_to_send = ContentFile(string_to_return.encode())
        response = HttpResponse(file_to_send,'text/plain')
        response['Content-Length'] = file_to_send.size
        disp = 'attachment; filename="{}_antislovari.txt"'.format(unidecode(request.session["string"]))
        response['Content-Disposition'] = disp
        return response
    elif request.method == "POST" and 'search_button' in request.POST:
        header = {"Content-type": "application/json"}
        # print(request.POST)
        json_to_send = request.POST.copy()
        json_to_send['tables'] = request.POST.getlist('tables')
        r = requests.post('{}/query'.format(API_LINK), json=json_to_send, headers=header)
        print('RETURN IS ', r.text)
        string_to_return = r.text
        request.session['string_to_return'] = string_to_return
        request.session['string'] = request.POST['string']
        return render(request, 'index.html', {'out': string_to_return.split()[:10]})
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
