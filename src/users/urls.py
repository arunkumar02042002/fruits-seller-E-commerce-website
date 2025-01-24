from django.urls import path

from users.views import CartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
]