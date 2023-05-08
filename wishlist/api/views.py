from django.shortcuts import render
from django.forms import ValidationError
from requests import Response
from rest_framework import generics, permissions , serializers , status
from django.views import generic
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from products.models import Product
from ..models import WishList
import users
from wishlist.api.pagination import WishListPagination
from .serializers import WishListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny ,IsAuthenticated


user = get_user_model()


class WishListView(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = WishListPagination

    def get_queryset(self):
        user = self.request.user
        return WishList.objects.filter(user=user)

    def get_object(self):
        user = self.request.user
        wishlist, created = WishList.objects.get_or_create(user=user)
        return wishlist


class UserWishlistDelete(generics.DestroyAPIView):
    serializer_class = WishListSerializer
    lookup_field = 'user'
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        wishlist = WishList.objects.get(user=user)
        return wishlist
    
    
class UserWishlistItemCreate(generics.CreateAPIView):
    serializer_class = WishListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        wishlist, _ = WishList.objects.get_or_create(user=user)
        products = serializer.validated_data.pop('product', [])
        for product in products:
            product_id = product['id']
            quantity = product['quantity']
            if wishlist.product.filter(id=product_id).exists():
                wishlist_item = wishlist.product.through.objects.get(product_id=product_id, wishlist_id=wishlist.id)
                wishlist_item.quantity += quantity
                wishlist_item.save()
            else:
                wishlist.product.add(product_id, through_defaults={'quantity': quantity})
        serializer.instance = wishlist
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)