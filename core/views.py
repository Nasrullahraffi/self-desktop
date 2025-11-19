"""
Core App Views
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.conf import settings
from .models import Profile, Project, SocialLink, Testimonial


def home_page(request):
    """Homepage view with featured content"""

    # Get profile (should only be one)
    profile = Profile.objects.filter(is_active=True).first()

    # Get featured projects
    featured_projects = Project.objects.filter(
        is_active=True,
        is_featured=True
    )[:6]

    # Get social links
    social_links = SocialLink.objects.filter(is_active=True)

    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:3]

    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'social_links': social_links,
        'testimonials': testimonials,
        'site_name': settings.SITE_NAME,
        'site_tagline': settings.SITE_TAGLINE,
        'home': 'active',
    }

    return render(request, 'core/core.html', context)


class ProjectListView(ListView):
    """List all projects"""
    model = Project
    template_name = 'core/projects_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        return Project.objects.filter(is_active=True)


class ProjectDetailView(DetailView):
    """Project detail view"""
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(is_active=True)


def about_page(request):
    """About page view"""

    profile = Profile.objects.filter(is_active=True).first()

    context = {
        'profile': profile,
        'about': 'active',
    }

    return render(request, 'core/about.html', context)


# Error handlers
def handler404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)


