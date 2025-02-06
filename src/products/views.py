from django.db.models import Prefetch
from django.http import Http404
from django.views.generic import DetailView, TemplateView

from products.models import Product, ProductReview

# Create your views here.

class ShopView(TemplateView):
    template_name = 'products/shop.html'

class ShopDetailView(DetailView):
    template_name = 'products/shop_details.html'
    model = Product
    context_object_name = 'product'
    pk_url_kwarg = 'uuid'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(
            uuid__in=[self.object.uuid]
        )[:5]
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)

        obj = Product.objects.filter(
            uuid=pk
        ).prefetch_related('tags', 'reviews').first()

        if obj is None:
            raise Http404("Product Not Found!")
        
        return obj
