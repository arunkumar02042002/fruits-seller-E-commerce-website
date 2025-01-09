from testimonials.models import Testimonial


def top_testimonials(request):
    top_rated_testimonials = Testimonial.objects.filter(rating__in=("4", "5")).order_by(
        "-rating", "-created_at"
    )[:5]
    return dict(top_rated_testimonials=top_rated_testimonials)
