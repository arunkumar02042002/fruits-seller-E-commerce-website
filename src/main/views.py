from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages

from . import forms

User = get_user_model()



class HomeView(TemplateView):
    """Home view renders index.html"""
    template_name = "main/index.html"


class AboutUsView(TemplateView):
    """About view renders about.html"""
    template_name = "main/about.html"
