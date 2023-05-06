from django.db import models
# from django.contrib.auth.models import User
from products.models import Product
from django.contrib.auth import get_user_model

class Cart(models.Model):
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
