from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

import shortuuid

User = get_user_model()


class SignUpForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email, first_name, last_name and
    password.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn't match."),
        "first_name_empty": _("first_name can't be an empty string."),
    }
    password1 = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput, validators=[validate_password]
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )
    mobile_number = forms.CharField(
        label=_("Mobile"),
        max_length=10,
        min_length=10,
        required=False,
        help_text=_("Enter your mobile number."),
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "mobile_number")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email, is_active=True).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError(self.error_messages["first_name_empty"])
        return first_name

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = shortuuid.uuid()
        user.is_active = False
        if commit:
            user.save()
        return user
