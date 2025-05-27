from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from common.responses import reponse_201Created

from orders.handlers.create_order import CreateOrders
from orders.serializers import OrderSerializer


class CreateOrderView(GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        """Handle POST request to create an order."""
        context = CreateOrders(request).create_order()
        return reponse_201Created(
            payload=context,
            message="Order created successfully.",
        )
