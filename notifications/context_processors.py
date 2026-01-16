from django.db.models import Q

from messaging.models import Message

from .models import Notification


def unread_counts(request):
    if not request.user.is_authenticated:
        return {"unread_notifications": 0, "unread_messages": 0}
    unread_notifications = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).count()
    unread_messages = (
        Message.objects.filter(
            Q(thread__client=request.user) | Q(thread__freelancer=request.user),
            is_read=False,
        )
        .exclude(sender=request.user)
        .count()
    )
    recent_notifications = Notification.objects.filter(recipient=request.user)[:5]
    return {
        "unread_notifications": unread_notifications,
        "unread_messages": unread_messages,
        "recent_notifications": recent_notifications,
    }
