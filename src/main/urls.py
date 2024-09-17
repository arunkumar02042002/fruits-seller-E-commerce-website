from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home"),
    path("about/", view=views.AboutUsView.as_view(), name="about"),
    path("contact/", view=views.ContactUsView.as_view(), name="contact"),
]
