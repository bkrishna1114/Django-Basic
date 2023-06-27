from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

# Create your views here.

# def call():
#     x = 30
#     y = 20
#     return x

def hello(request):
    # x = call()
    # y = 34
    # queryset  = Product.objects.all()
    # queryset  = Product.objects.count()
    # try:
    #     queryset = Product.objects.get(pk=0)
    # except:
    #     pass
    # queryset = Product.objects.all().first()
    # list(queryset)

    # queryset = Product.objects.filter(unit_price__range=(1,10))
    # queryset = Product.objects.filter(collection__id=4)
    #contains...
    # queryset = Product.objects.filter(title__contains='coffee')
    # queryset = Product.objects.filter(title__icontains='coffee')
    # queryset = Product.objects.filter(title__istartswith='n')
    # queryset = Product.objects.filter(title__istartswith='n')
    # queryset = Product.objects.filter(title__endswith='n')
    # queryset = Product.objects.filter(title__endswith='n')
    # queryset = Product.objects.filter(last_update__year=2020)
    # queryset = Product.objects.filter(last_update__month=2)
    # queryset = Product.objects.filter(last_update__day=2)
    # queryset = Product.objects.filter(last_update__month__range=(1,3))
    #practice ...
    # queryset = Product.objects.filter(title__icontains='sho')
    # queryset = Product.objects.filter(collection_id=4)
    # queryset = Product.objects.filter(collection_id=4)
    # queryset = Product.objects.filter(collection_id=4)[0:5]
    queryset = Product.objects.filter(collection_id=4).order_by('last_update')
    return render(request,template_name='hello.html',context={'products':list(queryset)})


#Models......
 