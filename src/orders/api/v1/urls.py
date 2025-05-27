from django.urls import path, include

from orders.api.v1.views import CreateOrderView

urlpatterns = [
    path("create-order/", CreateOrderView.as_view(), name="create_order"),
]
