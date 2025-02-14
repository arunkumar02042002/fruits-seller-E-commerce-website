from decimal import Decimal

from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from common.responses import reponse_200OK, reponse_201Created, response_400BadRequest

from products.api.v1.filters import ProductFilter, TagFilter
from products.api.v1.serializers import (
    CheckCouponSerializer,
    ProductSerializer,
    ProductReviewSerializer,
    TagSerializer,
)

from products.models import Product, Tag
from products.utils import get_page_data

from users.db_utils import get_cart_from_request_obj, get_cart_total

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


class CheckCouponView(GenericAPIView):
    serializer_class = CheckCouponSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon = serializer.validated_data.get("code")

        cart = get_cart_from_request_obj(request)
        sub_total = get_cart_total(cart)

        if coupon.min_price_required > sub_total:
            return response_400BadRequest(
                "Coupon code is not valid.",
                payload={
                    "error": {
                        "code": [f"Minimum order price required {coupon.min_price_required}."]
                    }
                }
            )

        return reponse_200OK(
            "Coupon code applied successfully.",
            payload={
                "code": coupon.code,
                "discount": coupon.discount,
                "sub_total": sub_total,
                "delivery_fee": Decimal(99.00),
                "total": sub_total + Decimal(99.00),
                "discounted_total": sub_total + Decimal(99.00) - coupon.discount
            }
        )
    

class AddProductReviewAPIView(GenericAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]
    products = Product.objects.all()

    def post(self, request, uuid, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(self.products, uuid=uuid)
        serializer.validated_data["product"] = product
        serializer.validated_data["profile"] = request.user.profile
        serializer.save()

        return reponse_201Created(
            "Product review added successfully.",
            payload=serializer.data
        )
