from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=124)
    first_name = serializers.CharField(max_length=124)
    last_name = serializers.CharField(max_length=124)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate_username(self, value):
        user = User.objects.filter(username__iexact=value).exists()
        if user:
            raise serializers.ValidationError(_("Username already exists."))
        return value

    def validate_email(self, value):
        user = User.objects.filter(email__iexact=value).exists()
        if user:
            raise serializers.ValidationError(
                _("User already exists with this email.")
            )
        return value

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError(_("Passwords don't match."))
        password_validation.validate_password(passwd)
        return data

    def create(self, validated_data):
        """Handle user creation."""
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user


class TokenModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')
