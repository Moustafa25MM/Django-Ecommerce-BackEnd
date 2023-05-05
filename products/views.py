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
    
   

# Create your views here.
