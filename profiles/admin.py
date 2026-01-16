from django.contrib import admin

from .models import Education, FreelancerProfile, Project, ProjectScreenshot, Skill


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "location", "availability", "hourly_rate")
    search_fields = ("user__email", "user__username", "title", "location")
    list_filter = ("availability",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "years", "profile")
    search_fields = ("name", "profile__user__username")
    list_filter = ("level",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("school", "degree", "field", "profile")
    search_fields = ("school", "degree", "profile__user__username")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "created_at")
    search_fields = ("title", "profile__user__username")


@admin.register(ProjectScreenshot)
class ProjectScreenshotAdmin(admin.ModelAdmin):
    list_display = ("project", "caption")
