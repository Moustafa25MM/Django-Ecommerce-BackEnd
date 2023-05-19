from django.shortcuts import get_object_or_404, render
from .models import Product , Category
from .serializers import ProductSerializer , CategorySerializer
from rest_framework import generics
from rest_framework.generics import ListAPIView
from products.pagination import ProductPagination
from rest_framework.permissions import AllowAny

class CategoryList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListByCategory(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)

class ProductList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('search')
        print('Search term:', search_term)
        if search_term:
            queryset = Product.objects.filter(name__icontains=search_term) | Product.objects.filter(description__icontains=search_term)
            print('Filtered queryset:', queryset)
            return queryset
        else:
            return Product.objects.all()
        
        # Create your views here.
