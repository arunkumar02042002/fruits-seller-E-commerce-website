from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from authentication.tokens import account_activation_token
from authentication.forms import SignUpForm

from users.models import Profile

User = get_user_model()


# Create your views here.
class SignUpView(View, TemplateResponseMixin):
    form_class = SignUpForm
    template_name = "authentication/signup.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return self.render_to_response(context={"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        email = request.POST.get("email")
        User.objects.filter(email=email, is_active=False).delete()
        if form.is_valid() is False:
            return self.render_to_response(context={"form": form})

        user = form.save()
        current_site = get_current_site(request)
        mail_subject = "Activate your account."
        message = render_to_string(
            "authentication/acc_active_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = user.email

        try:
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=False,
            )
            messages.success(
                request,
                "We have sent a verification link to your email. Please verify your account!",
            )
        except Exception as e:
            print(e)
            form.add_error("", "Error Occurred while Sending Email, Try Again!")
            messages.error(request, "Error occurred while sending mail")
            return self.render_to_response({"form": form})
        return redirect("signup")


class AccountActivateView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.filter(pk=uid).first()
        except Exception as e:
            print(e)
            user = None

        if (
            user is not None
            and account_activation_token.check_token(user, token) is True
        ):
            user.is_active = True
            user.save()
            Profile.objects.create(user=user)
            messages.success(
                request, "Your account has been verified. Please login to continue!"
            )
            return redirect(reverse("login"))
        else:
            messages.error(
                request,
                "We couldn't find you! Please sign-up to our platform then login.",
            )
            return redirect(reverse("signup"))


class LoginUserView(LoginView):
    template_name = "authentication/login.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        response = super().get(request, *args, **kwargs)
        return response


class LogoutUserView(LogoutView):
    pass
