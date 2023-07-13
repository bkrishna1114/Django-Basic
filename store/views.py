from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.filters import ProductFilter
from . models import Collection, Product ,OrderItem, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer
from django.db.models.aggregates import Count
from rest_framework.views import APIView
# from rest_framework.mixins import ListModelMixin,CreateModelMixin
# from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

#Model viewset - These are responsibel for creating the url directly with routers by registering..
class ProductViewSet(ModelViewSet): 
    queryset = Product.objects.all()
    #generic filtering with retirve all products..
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fileds = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title','description']
    ordering_filter = ['unit_price','last_update']
    
    # lookup_field = 'id'

    #filtering the based on collection..basic filtering
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {"request":self.request} #definying the context here..
    
    def destroy(self, request, *args, **kwargs):
         if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
              return Response({'error':"product is associated with another item"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
         return super().destroy(request, *args, **kwargs)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    lookup_field = 'id'

    #destory method..
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['id']).count()>0:
            return Response({'error':'collection cannot be deleted becuase it inclued one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class ReviewsViewSet(ModelViewSet):
    # queryset = Review.objects.all() 
    serializer_class = ReviewSerializer

    #over write the queryset..
    def get_queryset(self):
        return Review.objects.select_related('product').filter(product_id=self.kwargs['product_pk']) #it will select same product reviews every time..

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


#create ListCreateAPIView class based view...
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer

#     def get_serializer_context(self):
#         return {"request":self.request} #definying the context here..


# model view set we can create update and delete in same class

# #apiview process
# class ProductDetails(APIView):
#     def get(self,request,id):
#         product = get_object_or_404(Product,pk = id)
#         serializer = ProductSerializer(product,context={'request':request})
#         data = serializer.data
#         return Response(data)
    
#     def put(self,request,id):
#         product = get_object_or_404(Product,pk = id)
#         serializer = ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
    
#     def delete(self,request,id):
#         product = get_object_or_404(Product,pk = id)
#         if product.orderitems.count()>0:
#             return Response({'error':"product is associated with another item"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response({"message":'successfully deleted'},status=status.HTTP_204_NO_CONTENT)


# RetriveupdateDestroy apiview()
# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer
#     lookup_field = 'id'

#     #destory method..
#     def destroy(self, request, *args, **kwargs):
#         if Product.objects.filter(collection_id=kwargs['id']).count()>0:
#             return Response({'error':'collection cannot be deleted becuase it inclued one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().destroy(request, *args, **kwargs)

# class CollectionList(ListCreateAPIView):   #using the listCreateAPI View we can make it very easily
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer
        
# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request,pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(
#         products_count=Count('products')),pk=pk
#         )
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#     elif request.method == 'DELETE':
#         if collection.products.count()>0:
#             return Response({'error':'collection cannot be deleted becuase it inclued one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

#functional views ()
# @api_view(['GET','POST']) #get all collections
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
