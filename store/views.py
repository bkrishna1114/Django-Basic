from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer
from django.db.models.aggregates import Count

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



@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
        products_count=Count('products')),pk=pk
        )
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        if collection.products.count()>0:
            return Response({'error':'collection cannot be deleted becuase it inclued one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST']) #get all collections
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
