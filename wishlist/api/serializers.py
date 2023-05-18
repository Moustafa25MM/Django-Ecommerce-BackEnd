from rest_framework import serializers
from wishlist.models import Wishlist
from products.serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination


class ProductDetailsPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'size'
    max_page_size = 10
    
class WishlistSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', many=True, read_only=True)


    class Meta:
        model = Wishlist
        fields = ['id', 'user','product','product_details']

class WishlistGetSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    def get_product_details(self, obj):
        queryset = obj.product.all()
        paginator = ProductDetailsPagination()
        result_page = paginator.paginate_queryset(queryset, self.context['request'])
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data).data
    
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product_details']