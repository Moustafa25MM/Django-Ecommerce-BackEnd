from django.contrib import admin
from cart.models import Cart, CartItem

class ProductInline(admin.TabularInline ,admin.StackedInline):
    model = CartItem
    extra = 1
    verbose_name_plural = 'Products'
    
class CartAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('get_cart_number', 'user')
        
    def get_cart_number(self, obj):
        return f"Cart {obj.pk}"
    get_cart_number.short_description = 'Cart Number'

admin.site.register(Cart, CartAdmin)

    
    