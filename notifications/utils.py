from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q

from messaging.models import Message

from .models import Notification


def _unread_message_count(user):
    return (
        Message.objects.filter(Q(thread__client=user) | Q(thread__freelancer=user), is_read=False)
        .exclude(sender=user)
        .count()
    )


def send_notification(recipient, verb, actor=None, target_url="", data=None):
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_url=target_url,
        data=data or {},
    )
    payload = {
        "id": notification.id,
        "verb": notification.verb,
        "actor": actor.full_name if actor else "",
        "target_url": notification.target_url,
        "created_at": notification.created_at.isoformat(),
        "unread_notifications": Notification.objects.filter(
            recipient=recipient, is_read=False
        ).count(),
        "unread_messages": _unread_message_count(recipient),
    }
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f"notifications_{recipient.id}", {"type": "notify", "notification": payload}
        )
    return notification
