from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer

# Create your views here.
# def product_list(request):
#     return HttpResponse('ok')


#get all the products... here... 
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset,many=True,context={'request':request})
        data = serializer.data
        return Response(data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
           
        
#get individual products detils...
@api_view(['GET','PUT','PATCH','DELETE'])
def product_details(request,id):
    product = get_object_or_404(Product,pk = id) #for using in both put and get and patch
    if request.method == 'GET':
        serializer = ProductSerializer(product,context={'request':request})
        data = serializer.data
        return Response(data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if product.orderitems.count()>0:
            return Response({'error':"product is associated with another item"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view()
def collection_detail(request,pk):
    collection = Collection.objects.get(pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)