from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Pref


class UserRegistrationAPITests(APITestCase):
    def setUp(self):
        self.pref = Pref.objects.create(name="Tokyo")
        self.url = "/accounts/register/"

    def test_register_user(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123",
            "password_confirmation": "StrongPass123",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully!")

    def test_duplicate_email(self):
        CustomUser.objects.create_user(
            username="existinguser", email="test@example.com", password="pass123"
        )
        data = {
            "username": "newuser",
            "email": "test@example.com",
            "password": "StrongPass123",
            "password_confirmation": "StrongPass123",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_passwords_do_not_match(self):
        data = {
            "username": "testuser",
            "email": "test5@example.com",
            "password": "StrongPass123",
            "password_confirmation": "DifferentPass123",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password_confirmation", response.data)

    def test_short_username(self):
        data = {
            "username": "ab",
            "email": "test6@example.com",
            "password": "StrongPass123",
            "password_confirmation": "StrongPass123",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_password_missing_uppercase(self):
        data = {
            "username": "testuser",
            "email": "test7@example.com",
            "password": "strongpass123",
            "password_confirmation": "strongpass123",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_password_missing_number(self):
        data = {
            "username": "testuser",
            "email": "test8@example.com",
            "password": "StrongPass",
            "password_confirmation": "StrongPass",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_weak_password(self):
        data = {
            "username": "testuser",
            "email": "test2@example.com",
            "password": "weakpass",
            "password_confirmation": "weakpass",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_invalid_tel(self):
        data = {
            "username": "testuser",
            "email": "test3@example.com",
            "password": "StrongPass123",
            "password_confirmation": "StrongPass123",
            "tel": "invalidtel",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("tel", response.data)

    def test_tel_too_short(self):
        data = {
            "username": "testuser",
            "email": "test9@example.com",
            "password": "StrongPass123",
            "password_confirmation": "StrongPass123",
            "tel": "123",
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("tel", response.data)

    def test_tel_too_long(self):
        data = {
            "username": "testuser",
            "email": "test10@example.com",
            "password": "StrongPass123",
            "password_confirmation": "StrongPass123",
            "tel": "0" * 25,  # 25 digits, too long
            "pref": self.pref.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("tel", response.data)

    def test_invalid_pref(self):
        data = {
            "username": "testuser",
            "email": "test4@example.com",
            "password": "StrongPass123",
            "password_confirmation": "StrongPass123",
            "tel": "09012345678",
            "pref": 9999,  # Invalid ID
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("pref", response.data)
