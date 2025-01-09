from django.urls import path, include

from contact.views import ContactUsView

urlpatterns = [
    path("", view=ContactUsView.as_view(), name="contact"),
]
