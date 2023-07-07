from decimal import Decimal
from rest_framework import serializers
from store.models import Product

class ProductSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=255,decimal_places=2)
    price_with_gst = serializers.SerializerMethodField(method_name='PriceWithTax')

    def PriceWithTax(self,product:Product):
        return product.unit_price + (product.unit_price)/ (Decimal(18))
        
    