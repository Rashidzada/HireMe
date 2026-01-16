from django.urls import path

from .views import ThreadDetailView, ThreadListView, post_message

app_name = "messaging"

urlpatterns = [
    path("", ThreadListView.as_view(), name="thread-list"),
    path("<int:pk>/", ThreadDetailView.as_view(), name="thread-detail"),
    path("<int:pk>/send/", post_message, name="post-message"),
]
