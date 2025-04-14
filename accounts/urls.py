from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register_form/", views.register_form, name="register"),
    path("prefs/", views.prefs_list, name="prefs_list"),
]
