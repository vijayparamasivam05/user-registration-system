from rest_framework import serializers
from .models import CustomUser, Pref
import re


class PrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pref
        fields = ["id", "name"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    tel = serializers.CharField(required=False, allow_blank=True)
    pref = serializers.PrimaryKeyRelatedField(
        queryset=Pref.objects.all(), allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
            "password_confirmation",
            "tel",
            "pref",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )
        return value

    def validate_tel(self, value):
        if CustomUser.objects.filter(tel=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must be numeric.")
        if value and len(value) > 20 or len(value) < 10:
            raise serializers.ValidationError(
                "Phone number must be less than 20 characters and more than 10 characters."
            )
        return value

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
