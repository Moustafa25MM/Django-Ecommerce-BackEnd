from rest_framework import serializers
from ..models import WishList
from products.serializers import ProductSerializer


class WishListSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        fields = ['id', 'user', 'product', 'quantity', 'product_details']
        read_only_fields = ['id', 'user', 'product_details']

    def validate_user(self, value):
        user = self.context['request'].user
        if value != user:
            raise serializers.ValidationError('Cannot create or update wishlist for another user.')
        return value

    def create(self, validated_data):
        user = validated_data['user']
        wishlist, created = WishList.objects.get_or_create(user=user)
        return wishlist

    def update(self, instance, validated_data):
        instance.product.set(validated_data.get('product', instance.product.all()))
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance