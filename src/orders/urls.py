from django.urls import path

from orders.views import CheckoutView, OrderSuccessView, OrderFailureView


urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('success/', OrderSuccessView.as_view(), name='order_success'),
    path('failed/', OrderFailureView.as_view(), name='order_failed'),
]
