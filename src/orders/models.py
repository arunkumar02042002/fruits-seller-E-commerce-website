from django.db import models

from common.models import BaseModel

from orders.choices import (
    OrderStatusChoices,
    PaymentMethodChoices,
    PaymentStatusChoices
)
from orders.constants import SHIPPING_CHARGE

from products.models import Coupon, Product

from users.models import Address, Profile

# Create your models here.
class Order(BaseModel):

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="orders"
    )
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE,
        null=True, blank=True
    )
    coupon_discount = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0.00, verbose_name="Discount from coupon."
    )
    shipping_address = models.ForeignKey(
        Address, on_delete=models.CASCADE,
        null=True, blank=True
    )
    shiping_charges = models.DecimalField(
        max_digits=10, decimal_places=2, default=SHIPPING_CHARGE
    )
    order_amount = models.DecimalField(
        verbose_name="Total amount of products in the order.",
        max_digits=10, decimal_places=2
    )
    total_amount = models.DecimalField(
        verbose_name="Total Amount including charges and discounts.",
        max_digits=10, decimal_places=2
    )
    status = models.IntegerField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NOT_SET
    )
    payment_status = models.IntegerField(
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING
    )
    payment_method = models.IntegerField(
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.NOT_SET
    )
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.coupon and self.status in OrderStatusChoices.order_initiated_status_list():
            self.coupon_discount = self.coupon.discount

    def __str__(self):
        return f"Order by profile:{self.profile_id}"

class ProductInOrder(BaseModel):
    
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="products"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.product_price = self.product.price
        self.discounted_price = self.product.discounted_price
        
        self.total_price = self.discounted_price * self.quantity
        super(ProductInOrder, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product_id', 'order_id'], name='unique_order_product'
            )
        ]
    
    def __str__(self):
        return f"Order:{self.order_id}-Product:{self.product_id}"
