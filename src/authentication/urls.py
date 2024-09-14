from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("signup/", view=views.SignUpView.as_view(), name="signup"),
    path("login/", view=views.LoginUserView.as_view(), name="login"),
    path("logout/", view=views.LogoutUserView.as_view(), name="logout"),
    path(
        "activate/<uidb64>/<token>/",
        view=views.AccountActivateView.as_view(),
        name="activate-account",
    ),
    # Password Change
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="authentication/password_change.html",
            success_url=reverse_lazy("password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # Password Forget
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="authentication/password_reset.html",
            success_url=reverse_lazy("password_reset_sent"),
            email_template_name="authentication/forgot_password_email.html",
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="authentication/password_reset_sent.html",
        ),
        name="password_reset_sent",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_form.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html",
        ),
        name="password_reset_complete",
    ),
]
