from django.contrib import admin
from .models import Product , Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)