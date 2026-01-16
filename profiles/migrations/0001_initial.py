from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FreelancerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("profile_photo", models.ImageField(blank=True, null=True, upload_to="profiles/")),
                ("title", models.CharField(blank=True, max_length=120)),
                ("bio", models.TextField(blank=True)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("availability", models.CharField(choices=[("full_time", "Full-time"), ("part_time", "Part-time"), ("contract", "Contract"), ("not_available", "Not available")], default="not_available", max_length=20)),
                ("hourly_rate", models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("hide_contact_until_hired", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="freelancer_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("school", models.CharField(max_length=120)),
                ("degree", models.CharField(blank=True, max_length=120)),
                ("field", models.CharField(blank=True, max_length=120)),
                ("start_year", models.PositiveIntegerField(blank=True, null=True)),
                ("end_year", models.PositiveIntegerField(blank=True, null=True)),
                ("description", models.TextField(blank=True)),
                ("profile", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="education", to="profiles.freelancerprofile")),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField()),
                ("tech_stack", models.CharField(blank=True, max_length=200)),
                ("github_url", models.URLField(blank=True)),
                ("demo_url", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("profile", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="projects", to="profiles.freelancerprofile")),
            ],
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("level", models.CharField(choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")], max_length=20)),
                ("years", models.PositiveIntegerField(default=0)),
                ("profile", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="skills", to="profiles.freelancerprofile")),
            ],
        ),
        migrations.CreateModel(
            name="ProjectScreenshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="projects/screenshots/")),
                ("caption", models.CharField(blank=True, max_length=120)),
                ("project", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="screenshots", to="profiles.project")),
            ],
        ),
    ]
