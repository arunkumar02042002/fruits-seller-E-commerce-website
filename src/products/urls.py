from django.urls import path
from products.views import ShopView

urlpatterns = [
    path('shop/', view=ShopView.as_view(), name='shop'),
]