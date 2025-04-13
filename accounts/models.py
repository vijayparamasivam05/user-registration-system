from django.contrib.auth.models import AbstractUser
from django.db import models


# 都道府県モデル
class Pref(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# カスタムユーザーモデル
class CustomUser(AbstractUser):
    tel = models.CharField(max_length=20, null=True, blank=True)
    pref = models.ForeignKey(Pref, on_delete=models.SET_NULL, null=True, blank=True)
