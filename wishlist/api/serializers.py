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
        wishlist, _ = WishList.objects.get_or_create(user=user)
        return wishlist

    def update(self, instance, validated_data):
        products = validated_data.pop('product', [])
        for product in products:
            product_id = product['id']
            quantity = product['quantity']
            if instance.product.filter(id=product_id).exists():
                wishlist_item = instance.product.through.objects.get(product_id=product_id, wishlist_id=instance.id)
                wishlist_item.quantity += quantity
                wishlist_item.save()
            else:
                instance.product.add(product_id, through_defaults={'quantity': quantity})
        instance.quantity = instance.product.through.objects.aggregate(models.Sum('quantity'))['quantity__sum']
        instance.save()
        return instance
