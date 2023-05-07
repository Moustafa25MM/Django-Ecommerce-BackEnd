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
from .serializers import WishListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny ,IsAuthenticated

user = get_user_model()

# class WishListList(generics.ListCreateAPIView):
#     permission_classes=[IsAuthenticated]
    
#     queryset = WishList.objects.all()
#     serializer_class = WishListSerializer
    
#     def perform_create(self, serializer):
#         user = self.request.user
#         product_id=self.request.data.get('product')
#         user_wishList = WishList.objects.filter(user=user)
        
#         print(user_wishList)
        
#         if user_wishList:
#             product_in_wishlist = user_wishList.product.filter(id=product_id).exists()
#             if product_in_wishlist:
#                 raise serializers.ValidationError('product already exists in this wishlist')
#             else:
#                 product = get_object_or_404(Product , id=product_id)
#                 user_wishList.product.add(product)
#                 user_wishList.save()
#                 print('product added to existing wishlist')
                
#         else:
#                 product = get_object_or_404(Product, id=product_id)
#                 new_wishlist = WishList.objects.create(user=user)
#                 new_wishlist.product.add(product)

#                 new_wishlist.save()
#                 print('product added to new wishlist')
                

# class WishlistDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = WishList.objects.all()
#     serializer_class = WishListSerializer

class UserWishlistRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = WishListSerializer
    lookup_field = 'user'
    permission_classes = [permissions.IsAuthenticated]

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