from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from messaging.models import Thread
from notifications.utils import send_notification
from profiles.models import FreelancerProfile

from .forms import HireRequestForm, HireRequestStatusForm
from .models import HireRequest


class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_client


class FreelancerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_freelancer


class HireRequestCreateView(LoginRequiredMixin, ClientRequiredMixin, CreateView):
    template_name = "requests/hire_request_form.html"
    form_class = HireRequestForm

    def dispatch(self, request, *args, **kwargs):
        self.freelancer = get_object_or_404(
            FreelancerProfile, user__username=kwargs["username"], user__role="freelancer"
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.freelancer.user == self.request.user:
            messages.error(self.request, "You cannot send a request to yourself.")
            return redirect("marketplace:freelancer-detail", username=self.freelancer.user.username)
        with transaction.atomic():
            form.instance.client = self.request.user
            form.instance.freelancer = self.freelancer.user
            hire_request = form.save()
            Thread.objects.create(
                hire_request=hire_request,
                client=self.request.user,
                freelancer=self.freelancer.user,
            )
        send_notification(
            recipient=self.freelancer.user,
            actor=self.request.user,
            verb="sent you a hire request",
            target_url=reverse("requests:detail", args=[hire_request.pk]),
        )
        messages.success(self.request, "Hire request sent.")
        return redirect("requests:detail", pk=hire_request.pk)


class HireRequestDetailView(LoginRequiredMixin, DetailView):
    template_name = "requests/hire_request_detail.html"
    context_object_name = "hire_request"
    model = HireRequest

    def get_queryset(self):
        user = self.request.user
        return HireRequest.objects.select_related("client", "freelancer").filter(
            Q(client=user) | Q(freelancer=user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hire_request = context["hire_request"]
        context["thread"] = getattr(hire_request, "thread", None)
        return context


class HireRequestListView(LoginRequiredMixin, ListView):
    template_name = "requests/hire_request_list.html"
    context_object_name = "hire_requests"
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        return HireRequest.objects.select_related("client", "freelancer").filter(
            Q(client=user) | Q(freelancer=user)
        )


class HireRequestStatusUpdateView(LoginRequiredMixin, FreelancerRequiredMixin, UpdateView):
    template_name = "requests/hire_request_status.html"
    form_class = HireRequestStatusForm
    model = HireRequest

    def get_queryset(self):
        return HireRequest.objects.filter(
            freelancer=self.request.user, status=HireRequest.Status.PENDING
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        hire_request = self.object
        send_notification(
            recipient=hire_request.client,
            actor=self.request.user,
            verb=f"updated your hire request to {hire_request.status}",
            target_url=reverse("requests:detail", args=[hire_request.pk]),
        )
        messages.success(self.request, "Request status updated.")
        return response

    def get_success_url(self):
        return reverse_lazy("requests:detail", kwargs={"pk": self.object.pk})


@login_required
def cancel_request(request, pk):
    if request.method != "POST":
        return redirect("requests:detail", pk=pk)
    hire_request = get_object_or_404(
        HireRequest, pk=pk, client=request.user
    )
    hire_request.status = HireRequest.Status.CANCELLED
    hire_request.save(update_fields=["status", "updated_at"])
    send_notification(
        recipient=hire_request.freelancer,
        actor=request.user,
        verb="cancelled a hire request",
        target_url=reverse("requests:detail", args=[hire_request.pk]),
    )
    messages.info(request, "Hire request cancelled.")
    return redirect("requests:detail", pk=pk)
