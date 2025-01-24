from django.urls import path

from users.api.v1.views import (
    CartItemCreateAPIView,
    CartItemListAPIView,
    CartItemAPIView,
)

urlpatterns = [
    path('cart/', CartItemListAPIView.as_view(), name='cart-item-list'),
    path('cart/add/', CartItemCreateAPIView.as_view(), name='cart-item-create'),
    path('cart/<uuid:uuid>/', CartItemAPIView.as_view(), name='cart-item-retrieve-update-destroy'),
]