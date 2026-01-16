from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from .forms import (
    EducationForm,
    FreelancerProfileForm,
    ProjectForm,
    ProjectScreenshotForm,
    SkillForm,
)
from .models import Education, FreelancerProfile, Project, ProjectScreenshot, Skill


class FreelancerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_freelancer


class ProfileOverviewView(LoginRequiredMixin, FreelancerRequiredMixin, TemplateView):
    template_name = "profiles/profile_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = FreelancerProfile.objects.get_or_create(user=self.request.user)
        context.update(
            {
                "profile": profile,
                "skills": profile.skills.all(),
                "education": profile.education.all(),
                "projects": profile.projects.all(),
            }
        )
        return context


class FreelancerProfileUpdateView(LoginRequiredMixin, FreelancerRequiredMixin, UpdateView):
    template_name = "profiles/profile_form.html"
    form_class = FreelancerProfileForm
    success_url = reverse_lazy("profiles:overview")

    def get_object(self, queryset=None):
        profile, _ = FreelancerProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Profile updated.")
        return super().form_valid(form)


class SkillCreateView(LoginRequiredMixin, FreelancerRequiredMixin, CreateView):
    template_name = "profiles/skill_form.html"
    form_class = SkillForm
    success_url = reverse_lazy("profiles:overview")

    def form_valid(self, form):
        profile = get_object_or_404(FreelancerProfile, user=self.request.user)
        form.instance.profile = profile
        messages.success(self.request, "Skill added.")
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, FreelancerRequiredMixin, UpdateView):
    template_name = "profiles/skill_form.html"
    form_class = SkillForm
    success_url = reverse_lazy("profiles:overview")

    def get_queryset(self):
        return Skill.objects.filter(profile__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Skill updated.")
        return super().form_valid(form)


class SkillDeleteView(LoginRequiredMixin, FreelancerRequiredMixin, DeleteView):
    template_name = "profiles/confirm_delete.html"
    success_url = reverse_lazy("profiles:overview")

    def get_queryset(self):
        return Skill.objects.filter(profile__user=self.request.user)


class EducationCreateView(LoginRequiredMixin, FreelancerRequiredMixin, CreateView):
    template_name = "profiles/education_form.html"
    form_class = EducationForm
    success_url = reverse_lazy("profiles:overview")

    def form_valid(self, form):
        profile = get_object_or_404(FreelancerProfile, user=self.request.user)
        form.instance.profile = profile
        messages.success(self.request, "Education added.")
        return super().form_valid(form)


class EducationUpdateView(LoginRequiredMixin, FreelancerRequiredMixin, UpdateView):
    template_name = "profiles/education_form.html"
    form_class = EducationForm
    success_url = reverse_lazy("profiles:overview")

    def get_queryset(self):
        return Education.objects.filter(profile__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Education updated.")
        return super().form_valid(form)


class EducationDeleteView(LoginRequiredMixin, FreelancerRequiredMixin, DeleteView):
    template_name = "profiles/confirm_delete.html"
    success_url = reverse_lazy("profiles:overview")

    def get_queryset(self):
        return Education.objects.filter(profile__user=self.request.user)


class ProjectCreateView(LoginRequiredMixin, FreelancerRequiredMixin, CreateView):
    template_name = "profiles/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("profiles:overview")

    def form_valid(self, form):
        profile = get_object_or_404(FreelancerProfile, user=self.request.user)
        form.instance.profile = profile
        messages.success(self.request, "Project added.")
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, FreelancerRequiredMixin, UpdateView):
    template_name = "profiles/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("profiles:overview")

    def get_queryset(self):
        return Project.objects.filter(profile__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Project updated.")
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, FreelancerRequiredMixin, DeleteView):
    template_name = "profiles/confirm_delete.html"
    success_url = reverse_lazy("profiles:overview")

    def get_queryset(self):
        return Project.objects.filter(profile__user=self.request.user)


class ProjectScreenshotCreateView(LoginRequiredMixin, FreelancerRequiredMixin, CreateView):
    template_name = "profiles/screenshot_form.html"
    form_class = ProjectScreenshotForm

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(
            Project, pk=kwargs["project_id"], profile__user=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        messages.success(self.request, "Screenshot added.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("profiles:overview")


class ProjectScreenshotDeleteView(LoginRequiredMixin, FreelancerRequiredMixin, DeleteView):
    template_name = "profiles/confirm_delete.html"
    success_url = reverse_lazy("profiles:overview")

    def get_queryset(self):
        return ProjectScreenshot.objects.filter(project__profile__user=self.request.user)
