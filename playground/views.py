from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def call():
    x = 30
    y = 20
    return x

def hello(request):
    x = call()
    y = 34
    return render(request,template_name='hello.html',context={'name':'Balu'})


#Models......
