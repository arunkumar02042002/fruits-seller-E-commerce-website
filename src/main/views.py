from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home view renders index.html"""
    template_name = "main/index.html"


class AboutUsView(TemplateView):
    """About view renders about.html"""
    template_name = "main/about.html"
