from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class ShopView(TemplateView):
    template_name = 'products/shop.html'
