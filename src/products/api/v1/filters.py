from django_filters import rest_framework as filters

from products.choices import ProductCategoryChoice
from products.models import Product, Tag


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.ChoiceFilter(
        field_name="category", choices=ProductCategoryChoice.choices
    )
    sub_category = filters.CharFilter(
        field_name="sub_category", lookup_expr="icontains"
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__title",
        to_field_name="title",
        queryset=Tag.objects.all(),
        conjoined=True,
    )
    min_discount = filters.NumberFilter(
        field_name="discount_in_percent", lookup_expr="gte"
    )
    max_discount = filters.NumberFilter(
        field_name="discount_in_percent", lookup_expr="lte"
    )
    min_price = filters.NumberFilter(
        field_name="price", lookup_expr="gte"
    )
    max_price = filters.NumberFilter(
        field_name="price", lookup_expr="lte"
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "sub_category",
            "tags",
        ]
