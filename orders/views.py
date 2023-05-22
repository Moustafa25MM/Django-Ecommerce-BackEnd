from django.http import JsonResponse
from .serializers import  OrderSerializers,OrderItemsSerializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from stripe.error import AuthenticationError
from rest_framework.views import APIView
from cart.models import Cart,CartItem
from users.models import CustomUser
from django.shortcuts import redirect
from .models import Order,OrderItems,PaymentToken
from rest_framework import generics
from rest_framework import status
from django.db import transaction
from django.conf import settings
import stripe
import secrets


stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

class OrdertList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)



class CreateCheckout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        # validation before checkout
        if not cart_items:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        for item in cart_items:
            if item.quantity > item.product.available_quantity:
                return Response({'detail': f"Sorry, we do not have enough stock for {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)

        #make checkout Session
        line_items = []
        for item in cart_items:
            product_name = item.product.name
            price = item.product.price * 100  # Stripe requires the price in cents
            line_item = {
                'price_data' :{
                    'currency' : 'usd',  
                    'product_data': {
                        'name': product_name,
                    },
                    'unit_amount': int(price)
                },
                'quantity' : item.quantity
            }
            line_items.append(line_item)
        try:
            token = secrets.token_hex(16) # generate payment token
            base_url = request.scheme + '://' + request.get_host()
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,  # include the line_items parameter here
                mode='payment',
                success_url= f'{base_url}/orders/create?token={token}&user={user.id}',
                cancel_url= f'{base_url}/orders/create',
                )
            pToken = PaymentToken(user=user,Ptoken=token,status=True)
            pToken.save()
        except AuthenticationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # return redirect(checkout_session.url , code=303)
        return Response({'url': checkout_session.url})




# class WebHook(APIView):
#     def post(self , request):
#         event = None
#         payload = request.body
#         sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#         webhook_secret = settings.STRIPE_WEBHOOK_SECRET

#         try:
#             event = stripe.Webhook.construct_event(
#                 payload ,sig_header , webhook_secret
#                 )
#         except ValueError as err:
#             # Invalid payload
#             raise err
#         except stripe.error.SignatureVerificationError as err:
#             # Invalid signature
#             raise err

#         # Handle the event
#         if event.type == 'payment_intent.succeeded':
#             payment_intent = event.data.object 
#             print("--------payment_intent ---------->" , payment_intent)
#         elif event.type == 'payment_method.attached':
#             payment_method = event.data.object 
#             print("--------payment_method ---------->" , payment_method)
#         # ... handle other event types
#         else:
#             print('Unhandled event type {}'.format(event.type))
#         data = {
#                 'message': 'Hello, world!',
#                 'count': 42,
#                 'success':True,
#             }
#         return JsonResponse(safe=False,data=data)


class OrdertCreate(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    
    def get_queryset(self):
        return Order.objects.all()


    @transaction.atomic
    def get(self, request, *args, **kwargs):
        token = self.request.GET.get('token')
        user = self.request.GET.get('user')
        pToken = PaymentToken.objects.get(user=user,Ptoken=token,status=True) # check the token is valid
        if not pToken:
            return Response({"detail": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)
        pToken.status=False
        pToken.save()

        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart.id)

        total_price = 0
        for item in cart_items:
            total_price += item.quantity * item.product.price

        user = CustomUser.objects.get(id=user)  
        order = Order(user=user, total_price=total_price, status='pending')
        order.save()
        
        for item in cart_items:
            order_item = OrderItems(order=order, product=item.product,price=item.product.price,quantity=item.quantity)
            order_item.save()
            product = item.product
            product.available_quantity -= item.quantity
            product.save()
        
        cart_items.delete()
        
        serializer = OrderSerializers(order)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return redirect('http://localhost:3000/orders')



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

