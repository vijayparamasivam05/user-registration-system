from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "accounts/register_done.html")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})
