from rest_framework import serializers

from django.contrib.auth import get_user_model

from users.models import Address, Profile

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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'uuid', 'address_line', 'near_by',
            'city', 'state', 'country', 'pincode',
            'type'
        ]
        read_only_fields = ['uuid']

    def save(self, **kwargs):
        """Override save method to set profile."""
        profile = kwargs.get('profile')
        if not profile:
            raise serializers.ValidationError(
                "Profile is required to save address.")
        self.validated_data['profile'] = profile
        return super().save(**kwargs)


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'mobile_number',
        ]
