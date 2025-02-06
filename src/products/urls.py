from django.urls import path
from products.views import ShopDetailView, ShopView

urlpatterns = [
    path('shop/', view=ShopView.as_view(), name='shop'),
    path('shop/<uuid:uuid>/', view=ShopDetailView.as_view(), name='shop-detail'),
]