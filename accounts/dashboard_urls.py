from django.urls import path

from .views import ClientDashboardView, FreelancerDashboardView

app_name = "dashboard"

urlpatterns = [
    path("freelancer/", FreelancerDashboardView.as_view(), name="freelancer-dashboard"),
    path("client/", ClientDashboardView.as_view(), name="client-dashboard"),
]
