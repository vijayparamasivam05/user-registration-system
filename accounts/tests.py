from django.test import TestCase
from .models import CustomUser, Pref
from .forms import CustomUserCreationForm


class CustomUserFormTests(TestCase):

    def setUp(self):
        # Add a valid prefecture for testing
        self.pref = Pref.objects.create(name="Tokyo")

    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_username_too_short(self):
        form_data = {
            "username": "aa",
            "email": "test@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_duplicate_email(self):
        CustomUser.objects.create_user(
            username="existing", email="test@example.com", password="pass"
        )
        form_data = {
            "username": "newuser",
            "email": "test@example.com",  # same email
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_weak_password(self):
        form_data = {
            "username": "testuser",
            "email": "test2@example.com",
            "password1": "weakpass",
            "password2": "weakpass",
            "tel": "09012345678",
            "pref": self.pref.id,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_invalid_tel(self):
        form_data = {
            "username": "testuser",
            "email": "test3@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "tel": "abc123",  # Invalid
            "pref": self.pref.id,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("tel", form.errors)

    def test_invalid_pref(self):
        form_data = {
            "username": "testuser",
            "email": "test4@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "tel": "09012345678",
            "pref": 9999,  # Non-existent Pref ID
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("pref", form.errors)
