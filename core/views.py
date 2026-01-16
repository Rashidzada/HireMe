from django.http import HttpResponse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "core/home.html"
    extra_context = {
        "meta_title": "HireMe | Freelance Marketplace",
        "meta_description": "HireMe helps clients find freelancers fast with profiles, requests, and real-time chat.",
    }


class AboutView(TemplateView):
    template_name = "core/about.html"
    extra_context = {
        "meta_title": "About HireMe",
        "meta_description": "Learn about HireMe, a mini freelance marketplace for fast collaboration.",
    }


class ContactView(TemplateView):
    template_name = "core/contact.html"
    extra_context = {
        "meta_title": "Contact HireMe",
        "meta_description": "Get in touch with HireMe support and team.",
    }


class TermsView(TemplateView):
    template_name = "core/terms.html"
    extra_context = {
        "meta_title": "HireMe Terms",
        "meta_description": "HireMe terms and conditions for using the platform.",
    }


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow:",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
