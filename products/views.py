from django.shortcuts import get_object_or_404, render
from .models import Product , Category
from .serializers import ProductSerializer , CategorySerializer
from rest_framework import generics
from rest_framework.generics import ListAPIView
from products.pagination import ProductPagination

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListByCategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(categoryid=category_id)

class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('search')
        print('Search term:', search_term)
        if search_term:
            queryset = Product.objects.filter(nameicontains=search_term) | Product.objects.filter(description__icontains=search_term)
            print('Filtered queryset:', queryset)
            return queryset
        else:
            return Product.objects.all()
        
        # Create your views here.
