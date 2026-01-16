from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from notifications.utils import send_notification

from .models import Message, Thread


class ThreadDetailView(LoginRequiredMixin, DetailView):
    template_name = "messaging/thread_detail.html"
    context_object_name = "thread"
    model = Thread

    def get_queryset(self):
        user = self.request.user
        return (
            Thread.objects.select_related("client", "freelancer", "hire_request")
            .filter(Q(client=user) | Q(freelancer=user))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = context["thread"]
        messages_qs = thread.messages.select_related("sender")
        messages_qs.filter(is_read=False).exclude(sender=self.request.user).update(
            is_read=True
        )
        context["messages"] = messages_qs
        context["other_user"] = (
            thread.freelancer if self.request.user == thread.client else thread.client
        )
        return context


class ThreadListView(LoginRequiredMixin, ListView):
    template_name = "messaging/thread_list.html"
    context_object_name = "threads"

    def get_queryset(self):
        user = self.request.user
        return (
            Thread.objects.select_related("client", "freelancer", "hire_request")
            .filter(Q(client=user) | Q(freelancer=user))
            .order_by("-created_at")
        )


@login_required
def post_message(request, pk):
    if request.method != "POST":
        return redirect("messaging:thread-detail", pk=pk)
    thread = get_object_or_404(
        Thread.objects.filter(Q(client=request.user) | Q(freelancer=request.user)),
        pk=pk,
    )
    body = request.POST.get("body", "").strip()
    if body:
        message = Message.objects.create(thread=thread, sender=request.user, body=body)
        recipient = thread.freelancer if request.user == thread.client else thread.client
        send_notification(
            recipient=recipient,
            actor=request.user,
            verb="sent you a message",
            target_url=reverse("messaging:thread-detail", args=[thread.pk]),
            data={"thread_id": thread.pk},
        )
        messages.success(request, "Message sent.")
    return redirect("messaging:thread-detail", pk=pk)
