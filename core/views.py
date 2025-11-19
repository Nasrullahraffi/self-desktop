"""
Core App Views
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from .models import Profile, Project, SocialLink, Testimonial
from .forms import ProjectForm


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


# ==============================================================================
# PROJECT CRUD VIEWS
# ==============================================================================

class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Create new project"""
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing project"""
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete project"""
    model = Project
    template_name = 'core/project_confirm_delete.html'
    success_url = reverse_lazy('projects')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Error handlers
def handler404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)
