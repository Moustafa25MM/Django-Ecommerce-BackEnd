from django.contrib import admin
from wishlist.models import Wishlist

class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_list')

    def product_list(self, obj):
        return ", ".join([p.name for p in obj.product.all()])

admin.site.register(Wishlist, WishListAdmin)