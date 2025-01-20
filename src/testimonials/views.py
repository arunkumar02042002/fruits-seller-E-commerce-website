from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from testimonials.choices import TestimonialStatusChoices
from testimonials.forms import TestimonialCreateForm
from testimonials.models import Testimonial
from testimonials.tokens import testimonial_add_token

from users.dbio import UserDBIO

User = get_user_model()


class TestimonialAddView(View, TemplateResponseMixin):
    form_class = TestimonialCreateForm
    template_name = "testimonials/testimonial_form.html"

    def get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserDBIO.get_user_by_pk(pk=uid)
            return user
        except Exception as e:
            print(e)
            return None

    def validate_token(self, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and testimonial_add_token.check_token(user, token):
            return user
        return None

    def get(self, request, uuid, uidb64, token, *args, **kwargs):
        testimonial = get_object_or_404(Testimonial, pk=uuid)

        user = self.validate_token(uidb64, token)
        if user is None:
            messages.error("You tried to access a link that doesn't exists.")
            redirect("home")
        return self.render_to_response(
            request, self.template_name, {"form": self.form_class()}
        )

    def post(self, request, uuid, uidb64, token, *args, **kwargs):
        testimonial = get_object_or_404(Testimonial, pk=uuid)
        user = self.validate_token(uidb64, token)
        if user is None:
            messages.error("You tried to access a link that doesn't exists.")
            redirect("home")

        form = self.form_class(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.created_by = user
            testimonial.status = TestimonialStatusChoices.SUBMITTED
            testimonial.save()

            messages.success(request, "Testimonial submitted successfully.")
            return redirect("home")
        else:
            return self.render_to_response(request, self.template_name, {"form": form})
