from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'hello-world.html', {})

def healthz_view(request):
    return HttpResponse('Ok')