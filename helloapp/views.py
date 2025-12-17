from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse

def show_hello(request):
    return HttpResponse("ハロー、Django!")