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
            name="HireRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subject", models.CharField(max_length=150)),
                ("message", models.TextField()),
                ("budget", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("timeline", models.CharField(blank=True, max_length=120)),
                ("attachment", models.FileField(blank=True, null=True, upload_to="hire_requests/")),
                ("status", models.CharField(choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected"), ("cancelled", "Cancelled")], default="pending", max_length=20)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("client", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="hire_requests_sent", to=settings.AUTH_USER_MODEL)),
                ("freelancer", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="hire_requests_received", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
