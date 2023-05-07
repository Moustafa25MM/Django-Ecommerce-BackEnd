from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from users.models import CustomUser

# Create your models here.

class WishList(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE , related_name='wishlist' , blank=True)
    product = models.ManyToManyField(Product , related_name='wishlists')
    quantity = models.SmallIntegerField(default=1)
    
    def __str__(self):
        return self.user.username