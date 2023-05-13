from rest_framework import generics, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import AddToCartSerializer, UpdateCartSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated


class AddToCartView(generics.CreateAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateCartView(generics.UpdateAPIView):
    serializer_class = UpdateCartSerializer
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]


    def put(self, request, pk, *args, **kwargs):
        action = request.data.get('action')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(action=action)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    queryset = Cart.objects.all()
    lookup_field = 'user'
    
    
class DeleteCartItemView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    queryset = CartItem.objects.all()

    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)