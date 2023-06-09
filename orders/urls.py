from django.urls import path
from .views import *

urlpatterns = [
    path('', OrdertList.as_view(), name='order-list'),
    path('create/', OrdertCreate.as_view(), name='order-create'),
    
    
    path('checkout/', CreateCheckout.as_view(), name='order-checkout'),
    # path('webhook-test/' , WebHook.as_view()), 

    
    
    path('<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('<int:pk>/items/<int:item_pk>/', OrderItemsDetail.as_view(), name='order-item-detail'),

]
