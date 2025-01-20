from products.models import Product
from testimonials.models import Testimonial


def top_testimonials(request):
    """Return top rated testimonials."""
    top_rated_testimonials = Testimonial.objects.filter(
        rating__in=("4", "5")).order_by(
            "-rating", "-created_at"
        )[:5]
    return dict(top_rated_testimonials=top_rated_testimonials)

def featured_products(request):
    """Return featured products."""
    featured_products = Product.objects.filter(is_featured=True).order_by("-created_at")[:3]
    return dict(featured_products=featured_products)