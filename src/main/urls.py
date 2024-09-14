from django.urls import path

from . import views

urlpatterns = [path("", view=views.HomeView.as_view(), name="home")]
