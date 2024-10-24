from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages

from . import forms

User = get_user_model()


# Create your views here.
class HomeView(TemplateView):
    template_name = "main/index.html"


class AboutUsView(TemplateView):
    template_name = "main/about.html"


class ContactUsView(View, TemplateResponseMixin):
    form_class = forms.ContactUsForm
    template_name = "main/contact.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid() is False:
            return self.render_to_response(context={"form": form})

        email = form.cleaned_data["email"]
        contact_us = form.save(commit=False)
        contact_us.user = User.objects.filter(email=email).first()
        contact_us.save()
        messages.success(
            request,
            "Your query has been submitted. Our representative will contact you shortly.",
        )
        return redirect("contact")
