from rest_framework import serializers

from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
        ]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        exclude = [
            'deleted_at', 'created_by',
            'updated_by', 'deleted_by'
        ]
