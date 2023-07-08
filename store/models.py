from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

#Promotion - Product many to manay relation...
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # product 

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')

    def __str__(self) -> str:
        return self.title  #this will give the title in admin site
    

    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.CharField(max_length=255,null=True,blank=True)
    unit_price = models.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT,related_name='products') #protect the product on deleteing the collections
    promotions = models.ManyToManyField(Promotion,blank=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
        
#creating the Customer Model...
class Customer(models.Model):
    membership_bonze,membership_silver,membership_gold = 'B','S','G'
    MEMEBERSHIP_CHOICE = [
        (membership_bonze,'Bronze'),
        (membership_silver,'Silver'),
        (membership_gold,'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMEBERSHIP_CHOICE,default=membership_bonze)

    # class Meta:
    #     db_table = 'store_customers' #Changes the database table name..
    #     indexes = [
    #         models.Index(fields=['last_name','first_name','email']) #his will creat the index in the database in unique
    #     ]
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name','last_name']

class Order(models.Model):
    complete,failed,pending = 'C','F','P'
    PAYMENT_CHOICES = [
        (complete,'Complete'),
        (failed,'Failed'),
        (pending,'Pending')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_CHOICES,default=pending)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)


class Addresss(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # Customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True) #one to one realtion ship
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE) #one to one realtion ship

 
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


