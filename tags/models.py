from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TagItem(models.Model):
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    #Type (Product , video ,article)
    #ID
    content_type = models.ForeignKey(ContentType,on_delete= models.CASCADE) #content types user likes
    object_id = models.PositiveIntegerField()#object id that user like
    content_object = GenericForeignKey()#reading the actual object