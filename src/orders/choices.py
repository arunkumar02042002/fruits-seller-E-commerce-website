"""Choices for the orders app."""
from django.db.models import IntegerChoices

class OrderStatusChoices(IntegerChoices):
    NOT_SET = 0, 'Not Set'
    CREATED = 1, 'Created'
    PLACED = 2, 'Placed'
    SHIPPED = 3, 'Shipped'
    DELIVERED = 4, 'Delivered'
    CANCELLED = 5, 'Cancelled'
    RETURNED = 6, 'Returned'
    REFUNDED = 7, 'Refunded'
    FAILED = 8, 'Failed'

    @classmethod
    def order_initiated_status_list(cls):
        """Return list of unpaid order status."""
        return [
            OrderStatusChoices.NOT_SET,
            OrderStatusChoices.CREATED,
        ]  


class PaymentStatusChoices(IntegerChoices):
    PENDING = 0, 'Pending'
    SUCCESS = 1, 'Success'
    FAILED = 2, 'Failed'


class PaymentMethodChoices(IntegerChoices):
    NOT_SET = 0, 'Not Set'
    COD = 1, 'Cash on Delivery'
    RAZORPAY = 2, 'Razorpay'
