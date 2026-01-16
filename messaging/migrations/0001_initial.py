from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("requests", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Thread",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("client", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="client_threads", to=settings.AUTH_USER_MODEL)),
                ("freelancer", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="freelancer_threads", to=settings.AUTH_USER_MODEL)),
                ("hire_request", models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="thread", to="requests.hirerequest")),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_read", models.BooleanField(default=False)),
                ("sender", models.ForeignKey(on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("thread", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="messages", to="messaging.thread")),
            ],
            options={"ordering": ["created_at"]},
        ),
    ]
