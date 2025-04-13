from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "tel", "pref"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 3:
            raise forms.ValidationError("ユーザー名は3文字以上必要です。")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に使われています。")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise forms.ValidationError("パスワードは8文字以上必要です。")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("パスワードには大文字が必要です。")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("パスワードには小文字が必要です。")
        if not re.search(r"\d", password):
            raise forms.ValidationError("パスワードには数字が必要です。")
        return password

    def clean_tel(self):
        tel = self.cleaned_data.get("tel")
        if tel and not tel.isdigit():
            raise forms.ValidationError("電話番号は数字のみで入力してください。")
        return tel
