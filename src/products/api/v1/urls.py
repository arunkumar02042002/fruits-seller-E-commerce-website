
from django.urls import path

from products.api.v1.views import AddProductReviewAPIView, CheckCouponView, ProductListView, TagListView

urlpatterns = [
    path('', view=ProductListView.as_view(), name='products'),
    path('tags/', view=TagListView.as_view(), name='tags'),
    path('check-coupon/', view=CheckCouponView.as_view(), name='check-coupon'),
    path('products/<uuid:uuid>/add-review/', view=AddProductReviewAPIView.as_view(), name='add-review'),
]
