from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class EmailValidatorSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if User.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError("An user with that email already exists.")
        return email


class PasswordValidatorSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, validators=[validate_password])
