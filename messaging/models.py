from django.conf import settings
from django.db import models
from django.utils import timezone

from requests.models import HireRequest


class Thread(models.Model):
    hire_request = models.OneToOneField(
        HireRequest, on_delete=models.CASCADE, related_name="thread"
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_threads"
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="freelancer_threads"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Thread {self.pk} ({self.client.email} -> {self.freelancer.email})"


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message {self.pk} in Thread {self.thread_id}"
