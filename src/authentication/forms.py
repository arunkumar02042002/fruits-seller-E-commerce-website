from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

import shortuuid

User = get_user_model()


class SignUpForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255)
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput, validators=[validate_password]
    )
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email, is_active=True).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        try:
            user = User.objects.get(email=email, is_active=False)
            user.set_password(password)
        except User.DoesNotExist:
            username = shortuuid.uuid()
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.is_active = False
            user.save()
        return user
