import math

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from common.responses import reponse_200OK

from products.api.v1.filters import ProductFilter, TagFilter
from products.api.v1.serializers import ProductSerializer, TagSerializer

from products.models import Product, Tag
from products.utils import get_page_data

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend,)
    filterset_class = ProductFilter
    page_size = 9
    pagination_class = PageNumberPagination

    search_fields = ["name",  "sub_category", "description"]
    ordering_fields = ["created_at", "updated_at", "price", "discount_in_percent"]
    ordering = ["-created_at"]

    def list(self, request, *args, **kwargs):
        self.pagination_class.page_size = self.page_size
        response = super().list(request, *args, **kwargs)
        current = int(request.query_params.get('page', 1))
        count = response.data['count']

        return reponse_200OK(
            message="Products fetched successfully.",
            payload={
                **get_page_data(current, self.page_size, count),
                'results': response.data['results'],
            }
        )

    def get_queryset(self):
        return Product.objects.filter().prefetch_related("tags")


class TagListView(ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filterset_class = TagFilter
    ordering = ["title", "-created_at"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return reponse_200OK(
            message="Tags fetched successfully.",
            payload={"tags": response.data}
        )
