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
            raise serializers.ValidationError(
                "ユーザー名は3文字以上で入力してください。"
            )
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "このメールアドレスはすでに使用されています。"
            )
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "パスワードは8文字以上である必要があります。"
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "パスワードには1つ以上の大文字を含めてください。"
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "パスワードには1つ以上の小文字を含めてください。"
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "パスワードには1つ以上の数字を含めてください。"
            )
        return value

    def validate_tel(self, value):
        if CustomUser.objects.filter(tel=value).exists():
            raise serializers.ValidationError("この電話番号はすでに使用されています。")
        if value and not value.isdigit():
            raise serializers.ValidationError("電話番号は数字のみで入力してください。")
        if value and (len(value) < 10 or len(value) > 20):
            raise serializers.ValidationError(
                "電話番号は10文字以上20文字以下である必要があります。"
            )
        return value

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "パスワードが一致しません。"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
