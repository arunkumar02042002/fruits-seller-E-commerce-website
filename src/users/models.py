from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel

from products.models import Product

from users.choices import AddressChoices

User = get_user_model()


# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        upload_to="users/profile_pictures", blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to="users/cover_photos", blank=True, null=True
    )
    mobile = models.CharField(
        max_length=10, blank=True,
        null=True, unique=True,
        db_index=True, verbose_name='Mobile Number'
    )
    alternate_number = models.CharField(
        max_length=10, blank=True, null=True,
        unique=True, db_index=True,
        verbose_name='Alternate Number',
    )

    def full_address(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}, {self.pin_code}"

    def __str__(self):
        return f"{self.user.email}_{self.user.role}"

class Address(BaseModel):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    address_line = models.CharField(max_length=250, blank=True, null=True)
    near_by = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)

    type = models.CharField(
        max_length=20, choices=AddressChoices, 
        default=AddressChoices.HOME
    )

    # To locate user
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)

    def full_address(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}, {self.pin_code}"

class Cart(BaseModel):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='cart',
        null=True, blank=True
    )

    ip_address = models.GenericIPAddressField(
        blank=True, null=True
    )

    def __str__(self):
        return  f"profile-{self.profile_id}-cart"
    
class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE,
        related_name='cart_items'
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
    product_discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
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
        self.product_discounted_price = self.product.discounted_price
        
        self.total_price = self.product_discounted_price * self.quantity
        super(CartItem, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product_id', 'cart_id'], name='unique_cart_product'
            )
        ]

    def __str__(self) -> str:
        return 'cart_'+str(self.cart_id)+ '-product-'+str(self.product_id)
