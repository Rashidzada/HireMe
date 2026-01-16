from django.urls import path

from .views import (
    EducationCreateView,
    EducationDeleteView,
    EducationUpdateView,
    FreelancerProfileUpdateView,
    ProfileOverviewView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectScreenshotCreateView,
    ProjectScreenshotDeleteView,
    ProjectUpdateView,
    SkillCreateView,
    SkillDeleteView,
    SkillUpdateView,
)

app_name = "profiles"

urlpatterns = [
    path("", ProfileOverviewView.as_view(), name="overview"),
    path("edit/", FreelancerProfileUpdateView.as_view(), name="edit"),
    path("skills/add/", SkillCreateView.as_view(), name="skill-add"),
    path("skills/<int:pk>/edit/", SkillUpdateView.as_view(), name="skill-edit"),
    path("skills/<int:pk>/delete/", SkillDeleteView.as_view(), name="skill-delete"),
    path("education/add/", EducationCreateView.as_view(), name="education-add"),
    path("education/<int:pk>/edit/", EducationUpdateView.as_view(), name="education-edit"),
    path("education/<int:pk>/delete/", EducationDeleteView.as_view(), name="education-delete"),
    path("projects/add/", ProjectCreateView.as_view(), name="project-add"),
    path("projects/<int:pk>/edit/", ProjectUpdateView.as_view(), name="project-edit"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
    path(
        "projects/<int:project_id>/screenshots/add/",
        ProjectScreenshotCreateView.as_view(),
        name="screenshot-add",
    ),
    path(
        "screenshots/<int:pk>/delete/",
        ProjectScreenshotDeleteView.as_view(),
        name="screenshot-delete",
    ),
]
