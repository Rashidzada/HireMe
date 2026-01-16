from django.contrib import admin

from .models import HireRequest


@admin.register(HireRequest)
class HireRequestAdmin(admin.ModelAdmin):
    list_display = ("subject", "client", "freelancer", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("subject", "client__email", "freelancer__email")
