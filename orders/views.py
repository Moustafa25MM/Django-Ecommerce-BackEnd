from rest_framework import generics
from rest_framework.response import Response
from .models import Order,OrderItems
from .serializers import  OrderSerializers,OrderItemsSerializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework import status

# Create your views here.

class OrdertList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class OrdertCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    
    # def get_queryset(self):
    #     return Order.objects.all()

def perform_create(self, serializer):
        user = self.request.user
        # get cart items that belongs to the user
        # check the quantity of each product  



class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    
    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status == 'pending':
            print(order)
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({'detail': 'Cannot delete order with status other than "pending".'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        pk = self.kwargs.get('pk')
        order = get_object_or_404(queryset , pk = pk )
        if order.user != user:
            self.permission_denied(self.request)
        return order


class OrderItemsDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemsSerializers


    def get_object(self):
        pk = self.kwargs.get('pk')
        item = self.kwargs.get('item_pk')
        order = Order.objects.get(pk=pk, user=self.request.user)
        try:
            item = order.items.get(pk=item)
            return item
        except OrderItems.DoesNotExist :
            raise NotFound("Order item not found")

