from django.test import TestCase
from django.urls import reverse

from .models import User


class AuthFlowTests(TestCase):
    def test_register_creates_user(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "freelancer@example.com",
                "username": "freelancer-one",
                "first_name": "Free",
                "last_name": "Lancer",
                "role": User.Role.FREELANCER,
                "password1": "StrongPass!123",
                "password2": "StrongPass!123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="freelancer@example.com").exists())

    def test_login_with_email(self):
        user = User.objects.create_user(
            email="client@example.com",
            username="client-user",
            password="StrongPass!123",
            role=User.Role.CLIENT,
        )
        response = self.client.post(
            reverse("accounts:login"),
            {"username": user.email, "password": "StrongPass!123"},
        )
        self.assertEqual(response.status_code, 302)
