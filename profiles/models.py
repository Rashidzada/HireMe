from django.conf import settings
from django.db import models
from django.utils import timezone


class FreelancerProfile(models.Model):
    class Availability(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        NOT_AVAILABLE = "not_available", "Not available"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="freelancer_profile"
    )
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    title = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    availability = models.CharField(
        max_length=20, choices=Availability.choices, default=Availability.NOT_AVAILABLE
    )
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    hide_contact_until_hired = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} profile"

    def completeness_percent(self):
        total = 7
        completed = 0
        if self.profile_photo:
            completed += 1
        if self.title:
            completed += 1
        if self.bio:
            completed += 1
        if self.location:
            completed += 1
        if self.skills.exists():
            completed += 1
        if self.education.exists():
            completed += 1
        if self.projects.exists():
            completed += 1
        return int((completed / total) * 100)


class Skill(models.Model):
    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    profile = models.ForeignKey(
        FreelancerProfile, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=Level.choices)
    years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.profile.user.username})"


class Education(models.Model):
    profile = models.ForeignKey(
        FreelancerProfile, on_delete=models.CASCADE, related_name="education"
    )
    school = models.CharField(max_length=120)
    degree = models.CharField(max_length=120, blank=True)
    field = models.CharField(max_length=120, blank=True)
    start_year = models.PositiveIntegerField(blank=True, null=True)
    end_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.school} ({self.profile.user.username})"


class Project(models.Model):
    profile = models.ForeignKey(
        FreelancerProfile, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, blank=True)
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.profile.user.username})"


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField(upload_to="projects/screenshots/")
    caption = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"Screenshot for {self.project.title}"
