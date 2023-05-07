"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from products.views import ProductListByCategory ,ProductList , CategoryDetail , CategoryList , ProductDetail


urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('categories/<int:category_id>/products/', ProductListByCategory.as_view(), name='product-list-by-category'),
    
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),


    path("carts/", include('cart.urls')),
    
    path('auth/' , include("users.api.urls")),

    path("orders/", include('orders.urls')),
    
    path('wishlist/',include('wishlist.api.urls')),
]

