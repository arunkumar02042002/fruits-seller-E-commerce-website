from django.db.models import DecimalField, ExpressionWrapper, F

from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from products.api.v1.filters import ProductFilter
from products.api.v1.serializers import ProductSerializer

from products.models import Product


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend,)
    filterset_class = ProductFilter
    page_size = 9
    pagination_class = PageNumberPagination

    search_fields = ["name", "category", "tags__title"]
    ordering_fields = ["created_at", "updated_at", "price", "discount_in_percent"]
    ordering = ["-created_at"]

    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = self.page_size
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter().prefetch_related("tags")
