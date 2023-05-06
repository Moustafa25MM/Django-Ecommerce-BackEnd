from rest_framework import serializers
from .models import Order,OrderItems
from users.api.serializers import UserSerializer
from products.serializers import ProductSerializer

class OrderItemsSerializers(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model=OrderItems
        fields='__all__'

class OrderSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    items = OrderItemsSerializers(many=True,read_only=True)
    class Meta:
        model=Order
        fields='__all__'
