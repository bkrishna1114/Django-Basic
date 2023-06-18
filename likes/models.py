from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.
class LikedItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) #user id
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE) #content types user likes
    object_id = models.PositiveIntegerField() #object id that user like
    content_object = GenericForeignKey() #reading the actual object