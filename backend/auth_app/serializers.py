from rest_framework import serializers
from django.contrib.auth import get_user_model

# User = get_user_model()
from auth_app.models import Users as User


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=255)

    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value).count() == 0:
            raise serializers.ValidationError("Phone number is already taken.")
        elif not value.isdecimal():
            raise serializers.ValidationError("Phone number must be in number format")
        elif len(value) != 11:
            raise serializers.ValidationError("Phone number must be 11 digit")
        return value

    def create(self, validated_data):
        name = validated_data.get("name")
        password = validated_data.get("password")
        phone_number = validated_data.get("phone_number")

        User.objects.create_user(
            name=name, phone_number=phone_number, password=password
        )
        return validated_data


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=255)
