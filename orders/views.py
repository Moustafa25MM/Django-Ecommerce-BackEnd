from .serializers import  OrderSerializers,OrderItemsSerializers
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from cart.models import Cart,CartItem
from .models import Order,OrderItems
from rest_framework import generics
from rest_framework import status
from django.db import transaction

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
    
    def get_queryset(self):
        return Order.objects.all()


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = 0
        for item in cart_items:
            total_price += item.quantity * item.product.price
            if item.quantity > item.product.available_quantity:
                return Response({'detail': f"Sorry, we do not have enough stock for {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)        
        order = Order(user=request.user, total_price=total_price, status='pending')
        order.save()
        
        for item in cart_items:
            order_item = OrderItems(order=order, product=item.product,price=item.product.price,quantity=item.quantity)
            order_item.save()
            product = item.product
            product.available_quantity -= item.quantity
            product.save()
        
        cart_items.delete()
        
        serializer = OrderSerializers(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    
    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status.lower() == 'pending':
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({'detail': 'Cannot delete order with status other than "pending".'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        if not request.user.is_staff:
            return Response({'detail': 'You are not authorized to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        return self.update(request, *args, **kwargs)
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        pk = self.kwargs.get('pk')
        if self.request.user.is_staff:
            return Order.objects.get(pk=pk)
        order = get_object_or_404(queryset , pk = pk )
        if order.user != user :
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

