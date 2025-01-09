from django.urls import path
from main.views import HomeView, AboutUsView


urlpatterns = [
    path("", view=HomeView.as_view(), name="home"),
    path("about/", view=AboutUsView.as_view(), name="about"),
]
