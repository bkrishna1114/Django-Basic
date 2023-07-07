from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Product
from .serializers import ProductSerializers

# Create your views here.
# def product_list(request):
#     return HttpResponse('ok')


#get all the products... here... 
@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serializer = ProductSerializers(queryset,many=True)
    data = serializer.data
    return Response(data)

#get individual products detils...
@api_view()
def product_details(request,id):
    product = get_object_or_404(Product,pk = id)
    serializer = ProductSerializers(product)
    data = serializer.data
    return Response(data)