from django.contrib import admin

from .models import Message, Thread


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "hire_request", "client", "freelancer", "created_at")
    search_fields = ("client__email", "freelancer__email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "sender", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("body", "sender__email")
