from django.db import models
from users.models import CustomUser
from products.models import Product
# Create your models here.

class Order(models.Model):
    status_Choices=(('pending', 'pending'),
                    ('shipped', 'shipped'),
                    ('delivered', 'delivered'))
    status = models.CharField(max_length=20, choices=status_Choices,default='pending')
    date_ordered = models.DateField(auto_now_add=True)
    date_shipped = models.DateField(null=True,blank=True)
    date_delivered = models.DateField(null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username+'__'+str(self.total_price)

class OrderItems(models.Model):
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_item_price(self):
        return self.quantity * self.price

    def get_product_name(self):
        return self.product.name
