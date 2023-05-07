from django.urls import path
from .views import AddToCartView, UpdateCartView, CartView, DeleteCartItemView


urlpatterns = [
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('update-cart/<int:pk>/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/<int:user>/', CartView.as_view(), name='cart'),
    path('delete-cart-item/<int:pk>/', DeleteCartItemView.as_view(), name='delete_cart_item'),
]