from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from common.throttles import RestrictDayThrottle, RestrictMinThrottle

from .serializers import TestimonialCreateSerializer


class TestimonialAddView(CreateAPIView):
    serializer_class = TestimonialCreateSerializer
    throttle_classes = (RestrictMinThrottle, RestrictDayThrottle)
    permission_classes = (IsAuthenticated,)
