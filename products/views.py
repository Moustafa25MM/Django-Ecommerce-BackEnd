from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # Get Product
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    # Update Product
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    # Delete Product
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)  

# Create your views here.
