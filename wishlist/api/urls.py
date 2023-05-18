from django.urls import path
from .views import WishlistList, WishlistDetail, WishlistItemDelete,UserWishlistList

urlpatterns = [
    path('', WishlistList.as_view(), name='wishlist-detail'),
    path('<int:pk>/', WishlistDetail.as_view(), name='wishlist-create'),
    path('user', UserWishlistList.as_view(), name='user-wishlist-list'),

    path('product/<int:id>/', WishlistItemDelete.as_view(), name='wishlist-update'),
]