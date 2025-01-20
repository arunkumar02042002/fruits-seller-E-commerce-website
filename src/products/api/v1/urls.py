
from django.urls import path

from products.api.v1.views import ProductListView, TagListView

urlpatterns = [
    path('', view=ProductListView.as_view(), name='products'),
    path('tags/', view=TagListView.as_view(), name='tags')
]
