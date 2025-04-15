from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, word.")

def some_url(request):
    return HttpResponse("Hello, some.")