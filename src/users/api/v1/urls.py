from django.urls import path

from users.api.v1.views import (
    AddressListCreateAPIView,
    CartItemCreateAPIView,
    CartItemListAPIView,
    CartItemAPIView,
    CartTotalView,
)

urlpatterns = [
    path('address/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('cart/', CartItemListAPIView.as_view(), name='cart-item-list'),
    path('cart/add/', CartItemCreateAPIView.as_view(), name='cart-item-create'),
    path('cart/total/', CartTotalView.as_view(), name='cart-total'),
    path('cart/<uuid:uuid>/', CartItemAPIView.as_view(), name='cart-item-retrieve-update-destroy'),
]