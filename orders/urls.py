from django.urls import path
from .views import *

urlpatterns = [
    path('', OrdertList.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetail.as_view(), name='order-detail'),
]
