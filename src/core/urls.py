"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("authentication/", include("authentication.urls")),
    path("contact/", include("contact.urls")),
    path("orders/", include("orders.urls")),
    path("products/", include("products.urls")),
    path("users/", include("users.urls")),
    # API Views
    path("api/v1/authentication/", include("authentication.api.v1.urls")),
    path("api/v1/orders/", include("orders.api.v1.urls")),
    path("api/v1/products/", include("products.api.v1.urls")),
    path("api/v1/users/", include("users.api.v1.urls")),
    # Third-party
    path("ckeditor5/", include('django_ckeditor_5.urls'))
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
