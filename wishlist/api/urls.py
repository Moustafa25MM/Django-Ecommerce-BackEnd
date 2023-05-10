from django.urls import path
from wishlist.api.views import UserWishlistItemCreate,WishListView,UserWishlistDelete

urlpatterns = [
    path('list', WishListView.as_view(), name='user-wishlist-list'),
    path('delete', UserWishlistDelete.as_view(), name='user-wishlist-list'),
    path('create', UserWishlistItemCreate.as_view(), name='create-wishlist'),
    
]   

