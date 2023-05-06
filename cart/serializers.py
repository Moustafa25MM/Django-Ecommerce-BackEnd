from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = CartItem
        # fields = ('id', 'product', 'quantity', 'date_added')
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    # cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        # fields = ('id', 'user', 'cart_items')
        fields = '__all__'
