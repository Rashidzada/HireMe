from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from profiles.models import FreelancerProfile


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return ["core:home", "core:about", "core:contact", "core:terms", "marketplace:freelancer-list"]

    def location(self, item):
        return reverse(item)


class FreelancerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return FreelancerProfile.objects.select_related("user").filter(user__role="freelancer")

    def location(self, obj):
        return reverse("marketplace:freelancer-detail", args=[obj.user.username])
