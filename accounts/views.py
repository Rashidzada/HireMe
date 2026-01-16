from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from messaging.models import Message
from notifications.models import Notification
from profiles.models import FreelancerProfile
from requests.models import HireRequest

from .forms import EmailAuthenticationForm, UserRegistrationForm


def _client_ip(request):
    return request.META.get("REMOTE_ADDR", "unknown")


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts:role-redirect")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if user.is_freelancer and not hasattr(user, "freelancer_profile"):
            FreelancerProfile.objects.create(user=user)
        messages.success(self.request, "Welcome to HireMe!")
        return super().form_valid(form)


class EmailLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        ip = _client_ip(request)
        lockout_key = f"login-lockout:{ip}"
        if cache.get(lockout_key):
            messages.error(request, "Too many attempts. Please try again later.")
            return self.render_to_response(self.get_context_data())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(60 * 60 * 24 * 14)
        else:
            self.request.session.set_expiry(0)
        cache.delete(f"login-attempts:{_client_ip(self.request)}")
        return response

    def form_invalid(self, form):
        ip = _client_ip(self.request)
        attempts_key = f"login-attempts:{ip}"
        lockout_key = f"login-lockout:{ip}"
        attempts = cache.get(attempts_key, 0) + 1
        cache.set(attempts_key, attempts, timeout=60 * 30)
        max_attempts = settings.LOGIN_RATE_LIMIT.get("MAX_ATTEMPTS", 5)
        lockout_seconds = settings.LOGIN_RATE_LIMIT.get("LOCKOUT_SECONDS", 300)
        if attempts >= max_attempts:
            cache.set(lockout_key, True, timeout=lockout_seconds)
            cache.delete(attempts_key)
            messages.error(self.request, "Account locked. Please try again later.")
            return redirect("accounts:login")
        return super().form_invalid(form)


@login_required
def role_redirect(request):
    if request.user.is_freelancer:
        return redirect("dashboard:freelancer-dashboard")
    return redirect("dashboard:client-dashboard")


class FreelancerDashboardView(TemplateView):
    template_name = "accounts/dashboard_freelancer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = getattr(user, "freelancer_profile", None)
        requests_qs = HireRequest.objects.filter(freelancer=user)
        context.update(
            {
                "stats": {
                    "requests_count": requests_qs.count(),
                    "unread_messages": Message.objects.filter(
                        thread__freelancer=user, is_read=False
                    ).exclude(sender=user).count(),
                    "profile_completeness": profile.completeness_percent()
                    if profile
                    else 0,
                },
                "recent_requests": requests_qs.order_by("-created_at")[:5],
                "recent_messages": Message.objects.filter(thread__freelancer=user)
                .order_by("-created_at")[:5],
                "alerts": Notification.objects.filter(recipient=user, is_read=False)[:5],
            }
        )
        return context


class ClientDashboardView(TemplateView):
    template_name = "accounts/dashboard_client.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        requests_qs = HireRequest.objects.filter(client=user)
        context.update(
            {
                "stats": {
                    "requests_count": requests_qs.count(),
                    "unread_messages": Message.objects.filter(
                        thread__client=user, is_read=False
                    ).exclude(sender=user).count(),
                    "profile_completeness": 100,
                },
                "recent_requests": requests_qs.order_by("-created_at")[:5],
                "recent_messages": Message.objects.filter(thread__client=user)
                .order_by("-created_at")[:5],
                "alerts": Notification.objects.filter(recipient=user, is_read=False)[:5],
            }
        )
        return context
