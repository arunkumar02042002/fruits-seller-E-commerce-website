from django.db.models import Count

from products.models import Product

from testimonials.models import Testimonial

from users.models import Cart


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


def category_product_count(request):
    """Return count of products in each category."""
    categories_product_count = Product.objects.values(
        "category"
    ).annotate(
        count=Count("category")
    ).order_by("category")
    return dict(categories_product_count=categories_product_count)


def cart_items_count(request):
    """Return count of items in cart."""
    user = request.user
    ip = request.META.get("REMOTE_ADDR")

    if user.is_authenticated:
        count = Cart.objects.filter(profile__user=user).count()
    else:
        count = Cart.objects.filter(ip_address=ip, profile__isnull=True).count()

    return dict(cart_items_count=count)
