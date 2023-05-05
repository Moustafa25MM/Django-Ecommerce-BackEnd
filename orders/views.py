from rest_framework import generics
from .models import Order
from .serializers import  OrderSerializers
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class OrdertList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers