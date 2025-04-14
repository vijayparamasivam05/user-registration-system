from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserRegistrationSerializer, PrefSerializer
from django.shortcuts import render
from .forms import CustomUserCreationForm
from .models import Pref


# フォームベースの登録ビュー
def register_form(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "accounts/register_done.html")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


# Prefs API view
@api_view(["GET"])
def prefs_list(request):
    try:
        prefs = Pref.objects.all()
        serializer = PrefSerializer(prefs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": f"Something went wrong: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# APIベースの登録ビュー
@api_view(["POST"])
def register(request):
    try:
        if request.method == "POST":

            user_data = request.data

            serializer = UserRegistrationSerializer(data=user_data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(user_data["password"])
                user.save()

                return Response(
                    {"message": "User registered successfully!", "data": user_data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error": f"Something went wrong: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
