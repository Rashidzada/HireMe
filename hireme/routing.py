from django.urls import path

from messaging.consumers import ChatConsumer
from notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    path("ws/chat/<int:thread_id>/", ChatConsumer.as_asgi()),
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
