"""
Core App Views
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from .models import Profile, Project, SocialLink, Testimonial
from .forms import ProjectForm, ProfileForm


def home_page(request):
    """Homepage view with featured content"""

    # Get profile based on whether user is authenticated
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user, is_active=True).first()
        # Get user's featured projects
        featured_projects = Project.objects.filter(
            user=request.user,
            is_active=True,
            is_featured=True
        )[:6]
        # Get user's social links
        social_links = SocialLink.objects.filter(user=request.user, is_active=True)
        # Get user's testimonials
        testimonials = Testimonial.objects.filter(user=request.user, is_active=True)[:3]
    else:
        # For non-authenticated users, show nothing or default content
        profile = None
        featured_projects = []
        social_links = []
        testimonials = []

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


class ProjectListView(LoginRequiredMixin, ListView):
    """List all user's projects"""
    model = Project
    template_name = 'core/projects_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user, is_active=True)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Project detail view"""
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user, is_active=True)


def about_page(request):
    """About page view"""

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user, is_active=True).first()
    else:
        profile = None

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
        form.instance.user = self.request.user
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing project"""
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    success_url = reverse_lazy('projects')

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete project"""
    model = Project
    template_name = 'core/project_confirm_delete.html'
    success_url = reverse_lazy('projects')

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# PROFILE UPDATE VIEW
# ==============================================================================

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update profile information with image upload"""
    model = Profile
    form_class = ProfileForm
    template_name = 'core/profile_form.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """Get or create user's profile"""
        profile, created = Profile.objects.get_or_create(
            user=self.request.user,
            defaults={'full_name': self.request.user.get_full_name() or self.request.user.username}
        )
        return profile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


# Error handlers
def handler404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)
