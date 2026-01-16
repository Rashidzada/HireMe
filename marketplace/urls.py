from django.urls import path

from .views import FreelancerDetailView, FreelancerListView

app_name = "marketplace"

urlpatterns = [
    path("freelancers/", FreelancerListView.as_view(), name="freelancer-list"),
    path("freelancer/<slug:username>/", FreelancerDetailView.as_view(), name="freelancer-detail"),
]
