from django.urls import path

from . import views

urlpatterns = [
    path(
        "validate_password/",
        view=views.PasswordValidatorApiView.as_view(),
        name="validate-password",
    ),
    path(
        "validate_email/",
        view=views.EmailValidatorApiView.as_view(),
        name="validate-email",
    ),
]
