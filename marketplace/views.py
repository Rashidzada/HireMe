from django.db.models import Q
from django.views.generic import DetailView, ListView

from profiles.models import FreelancerProfile


class FreelancerListView(ListView):
    template_name = "marketplace/freelancer_list.html"
    context_object_name = "freelancers"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            FreelancerProfile.objects.select_related("user")
            .prefetch_related("skills")
            .filter(user__role="freelancer")
        )
        q = self.request.GET.get("q", "").strip()
        location = self.request.GET.get("location", "").strip()
        availability = self.request.GET.get("availability", "").strip()
        if q:
            queryset = queryset.filter(
                Q(user__first_name__icontains=q)
                | Q(user__last_name__icontains=q)
                | Q(user__username__icontains=q)
                | Q(title__icontains=q)
                | Q(skills__name__icontains=q)
            )
        if location:
            queryset = queryset.filter(location__icontains=location)
        if availability:
            queryset = queryset.filter(availability=availability)

        sort = self.request.GET.get("sort", "")
        sort_map = {
            "rate_asc": "hourly_rate",
            "rate_desc": "-hourly_rate",
            "name_asc": "user__username",
            "name_desc": "-user__username",
        }
        if sort in sort_map:
            queryset = queryset.order_by(sort_map[sort])
        else:
            queryset = queryset.order_by("-updated_at")
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
            "location": self.request.GET.get("location", ""),
            "availability": self.request.GET.get("availability", ""),
            "sort": self.request.GET.get("sort", ""),
        }
        context["availability_choices"] = FreelancerProfile.Availability.choices
        context["meta_title"] = "Browse Freelancers | HireMe"
        context["meta_description"] = "Search freelance profiles by skill, location, and availability."
        return context


class FreelancerDetailView(DetailView):
    template_name = "marketplace/freelancer_detail.html"
    context_object_name = "profile"

    def get_queryset(self):
        return (
            FreelancerProfile.objects.select_related("user")
            .prefetch_related("skills", "education", "projects", "projects__screenshots")
            .filter(user__role="freelancer")
        )

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        username = self.kwargs["username"]
        return queryset.get(user__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context["profile"]
        context["meta_title"] = f"{profile.user.full_name} | HireMe"
        context["meta_description"] = profile.bio[:160] if profile.bio else "Hire top freelance talent on HireMe."
        context["canonical_url"] = self.request.build_absolute_uri()
        context["can_request"] = (
            self.request.user.is_authenticated and self.request.user.is_client
        )
        return context
