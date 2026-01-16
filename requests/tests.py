from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from messaging.models import Thread
from profiles.models import FreelancerProfile

from .models import HireRequest


class HireRequestTests(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            email="client@example.com",
            username="client",
            password="StrongPass!123",
            role=User.Role.CLIENT,
        )
        self.freelancer_user = User.objects.create_user(
            email="freelancer@example.com",
            username="freelancer",
            password="StrongPass!123",
            role=User.Role.FREELANCER,
        )
        FreelancerProfile.objects.create(user=self.freelancer_user)

    def test_hire_request_creates_thread(self):
        self.client.login(username=self.client_user.email, password="StrongPass!123")
        response = self.client.post(
            reverse("requests:send", args=[self.freelancer_user.username]),
            {
                "subject": "Need a designer",
                "message": "Can you help with a landing page?",
                "budget": "500",
                "timeline": "2 weeks",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(HireRequest.objects.count(), 1)
        self.assertEqual(Thread.objects.count(), 1)
