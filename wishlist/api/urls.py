from django.urls import path
from wishlist.api.views import UserWishlistItemCreate,UserWishlistRetrieveUpdate,UserWishlistDelete

urlpatterns = [
    path('list', UserWishlistRetrieveUpdate.as_view(), name='user-wishlist-list'),
    path('delete', UserWishlistDelete.as_view(), name='user-wishlist-list'),
    path('create', UserWishlistItemCreate.as_view(), name='create-wishlist'),
    
]   

