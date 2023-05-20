from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'size'
    max_page_size = 15
    
class CategoryPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'size'
    max_page_size = 15