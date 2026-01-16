from django.urls import path

from .views import NotificationListView, mark_all_read, mark_read

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="list"),
    path("<int:pk>/read/", mark_read, name="mark-read"),
    path("read-all/", mark_all_read, name="mark-all-read"),
]
