from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from contact.choices import ContactUsStatusChoice
from contact.forms import ContactUsForm

from users.dbio import UserDBIO

# Create your views here.
class ContactUsView(View, TemplateResponseMixin):
    form_class = ContactUsForm
    template_name = "contact/contact.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid() is False:
            return self.render_to_response(context={"form": form})

        email = form.cleaned_data["email"]
        contact_us = form.save(commit=False)
        contact_us.created_by = UserDBIO.get_user_by_email(email=email)
        contact_us.status = ContactUsStatusChoice.PENDING
        contact_us.save()
        messages.success(
            request,
            "Your query has been submitted. Our representative will contact you shortly.",
        )
        return redirect("contact")
