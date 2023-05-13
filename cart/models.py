from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator
from users.models import CustomUser

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE , related_name='cart')
    products = models.ManyToManyField(Product, related_name='carts', through='CartItem')

    
    def __str__(self):
        return self.user.get_username()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)],default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
