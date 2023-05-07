from django.contrib import admin
from .models import WishList

class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_list' , 'quantity')

    def product_list(self, obj):
        return ", ".join([p.name for p in obj.product.all()])

admin.site.register(WishList, WishListAdmin)