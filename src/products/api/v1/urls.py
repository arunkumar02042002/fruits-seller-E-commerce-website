
from django.urls import path

from . import views

urlpatterns = [
    path('', view=views.ProductListView.as_view(), name='products')
]
