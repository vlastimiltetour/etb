from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the orders index.")
