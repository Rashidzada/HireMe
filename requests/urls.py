from django.urls import path

from .views import (
    HireRequestCreateView,
    HireRequestDetailView,
    HireRequestListView,
    HireRequestStatusUpdateView,
    cancel_request,
)

app_name = "requests"

urlpatterns = [
    path("", HireRequestListView.as_view(), name="list"),
    path("send/<slug:username>/", HireRequestCreateView.as_view(), name="send"),
    path("<int:pk>/", HireRequestDetailView.as_view(), name="detail"),
    path("<int:pk>/status/", HireRequestStatusUpdateView.as_view(), name="status"),
    path("<int:pk>/cancel/", cancel_request, name="cancel"),
]
