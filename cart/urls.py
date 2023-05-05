from django.urls import path
from .views import CartListCreateView, CartDetailView, CartItemCreateView, CartItemDetailView

urlpatterns = [
    path('', CartListCreateView.as_view(), name='cart-list'), #backend create this step
    path('<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('cartitems/', CartItemCreateView.as_view(), name='cartitem-create'),
    path('cartitems/<int:pk>/', CartItemDetailView.as_view(), name='cartitem-detail'),
]