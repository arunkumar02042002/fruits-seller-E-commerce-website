from django.contrib import admin

from .models import Coupon, Product, ProductTag, Tag

# Register your models here.
admin.site.register(Coupon)
admin.site.register(Product)
admin.site.register(ProductTag)
admin.site.register(Tag)