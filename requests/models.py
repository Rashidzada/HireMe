from django.conf import settings
from django.db import models
from django.utils import timezone


class HireRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hire_requests_sent"
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hire_requests_received"
    )
    subject = models.CharField(max_length=150)
    message = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    timeline = models.CharField(max_length=120, blank=True)
    attachment = models.FileField(upload_to="hire_requests/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} ({self.client.email} -> {self.freelancer.email})"
