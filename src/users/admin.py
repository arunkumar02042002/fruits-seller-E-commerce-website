from django.contrib import admin

from users.models import Address, Cart, CartItem, Profile

# Register your models here.
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Profile)