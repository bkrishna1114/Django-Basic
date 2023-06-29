from django.shortcuts import render
from django.http import HttpResponse
from store.models import *
from django.db.models import Q,F
from django.db.models.aggregates import Count,Max,Min,Avg,StdDev,Variance,Sum
from django.db.models import Value,Func
from django.db.models.functions import Concat


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
    # queryset = Product.objects.filter(collection_id=4).order_by('last_update')
    #multiple conditions..
    # queryset = Product.objects.filter(Q(unit_price__lte=30) & ~Q(unit_price__gte=20))
    # queryset = Product.objects.filter(Q(unit_price__lte=30) | ~Q(unit_price__gte=20))

    #comparing....referencing the fields...
    # queryset = Product.objects.filter(inventory = F('unit_price'))
    # queryset = Product.objects.filter(inventory__lt = F('unit_price'))
    # queryset = Product.objects.filter(inventory__gt = F('unit_price'))

    #sorting data....
    # queryset = Product.objects.order_by('title')
    # queryset = Product.objects.order_by('unit_price','-title')
    # queryset = Product.objects.order_by('unit_price','-title').reverse() #it will recerse the queries...
    # product = Product.objects.earliest('unit_price')
    # product = Product.objects.latest('unit_price')

    #limitig the results...
    # queryset = Product.objects.all()[10:15] 

    #selecting fields to queqy..
    # queryset = Product.objects.all()[10:15].values('id','title')
    # queryset = Product.objects.values('id','title','collection__title') #inner join
    #select products that have been ordered and sort them by title...
    # queryset =Product.objects.filter(id__in= OrderItem.objects.values('product_id').distinct()).order_by('title')

    #deffering method..
    # queryset = Product.objects.only('id','title')
    # queryset = Product.objects.defer('description')

    #select realated objects --(---- joins...)
    # queryset = Product.objects.select_related('collection').all()

    #prefetch method...()
    # queryset = Product.objects.prefetch_related('promotions').all() #prefetch the results...
    # queryset = Product.objects.prefetch_related('promotions').select_related('collection').all() #prefetch the results...

    #GEt the last 5 orders with their customer and items(incl product)
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[0:5]

    #aggrigate... functions..
    
    # agg = Product.objects.filter(collection__id=4).aggregate(Count('id'),Sum('unit_price'))
    # agg = Product.objects.aggregate(Avg('id'))
    # agg = Product.objects.aggregate(StdDev('unit_price'))
    # agg = Product.objects.aggregate(Variance('id'))
    
    
    #annotations...
    # queryset = Customer.objects.annotate(is_new=Value(True)) #this will add the new column called is_new=True
    queryset = Customer.objects.annotate(new_id=F('id') + 5)
    
    
    #Func
    # queryset = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'),function='CONCAT'))
    queryset = Customer.objects.annotate(full_name= Concat('first_name',Value(' '),'last_name'))


    return render(request,template_name='hello.html',context={'orders':queryset})


def practice(request):
    #get the all promotions data..
    # queryset = Promotion.objects.all()

    #get specfic product of ow matching...
    # queryset = Product.objects.get(id=2)

    #filtering ...
    # queryset = Customer.objects.filter(membership='B')

    #getting all prducts with price grater then $50
    # queryset = Product.objects.filter(~Q(collection__id=4)| Q(unit_price__lt=50))

    #gettinga all orders firstname and email..
    # queryset = Order.objects.select_related('customer').values('id','customer__first_name','customer__email')

    #Get the total quantity of a specific product sold across all orders:
    # queryset = OrderItem.objects.filter(product=8).aggregate(quantity=models.Sum('quantity'))


    #    Get all customers who have placed an order:
    queryset = Customer.objects.filter(order__isnull=False).distinct()
    

    return render(request,'practice.html',status=200,context={'data':list(queryset)})
 