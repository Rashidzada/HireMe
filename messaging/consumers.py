import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q

from notifications.utils import send_notification

from .models import Message, Thread


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope["url_route"]["kwargs"]["thread_id"]
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
        thread = await self._get_thread()
        if not thread:
            await self.close()
            return
        self.thread = thread
        self.group_name = f"thread_{self.thread_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            return
        body = payload.get("message", "").strip()
        if not body:
            return
        message = await self._create_message(body)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": {
                    "id": message.id,
                    "sender": message.sender.full_name,
                    "sender_id": message.sender_id,
                    "body": message.body,
                    "created_at": message.created_at.isoformat(),
                },
            },
        )
        await self._notify_recipient(message)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def _get_thread(self):
        return Thread.objects.filter(
            Q(client=self.user) | Q(freelancer=self.user), pk=self.thread_id
        ).first()

    @database_sync_to_async
    def _create_message(self, body):
        return Message.objects.create(thread=self.thread, sender=self.user, body=body)

    @database_sync_to_async
    def _notify_recipient(self, message):
        recipient = (
            self.thread.freelancer
            if message.sender_id == self.thread.client_id
            else self.thread.client
        )
        send_notification(
            recipient=recipient,
            actor=message.sender,
            verb="sent you a message",
            target_url=f"/messages/{self.thread.pk}/",
            data={"thread_id": self.thread.pk},
        )
