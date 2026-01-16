from django import forms

from core.forms import BootstrapFormMixin

from .models import Education, FreelancerProfile, Project, ProjectScreenshot, Skill


class FreelancerProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            "profile_photo",
            "title",
            "bio",
            "location",
            "availability",
            "hourly_rate",
            "phone",
            "hide_contact_until_hired",
        ]

    def clean_hourly_rate(self):
        hourly_rate = self.cleaned_data.get("hourly_rate")
        if hourly_rate is not None and hourly_rate < 0:
            raise forms.ValidationError("Hourly rate must be positive.")
        return hourly_rate


class SkillForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "level", "years"]


class EducationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Education
        fields = ["school", "degree", "field", "start_year", "end_year", "description"]


class ProjectForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "tech_stack", "github_url", "demo_url"]


class ProjectScreenshotForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ProjectScreenshot
        fields = ["image", "caption"]
