"""
Accounts App Views
Authentication and User Management
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
    UserProfileUpdateForm
)
from .models import UserProfile


class UserRegisterView(CreateView):
    """User registration view"""
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Save user and log them in"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Account created successfully for {form.cleaned_data.get("username")}! Please log in.'
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context


class UserLoginView(LoginView):
    """Custom login view"""
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirect to dashboard after login"""
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class UserLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


@login_required
def dashboard(request):
    """User dashboard - central hub for managing content"""
    from core.models import Project
    from education.models import Skill, Education, Certification
    from services.models import Service

    # Ensure user has a profile (create if doesn't exist)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, 'Profile created! Please update your information in Settings.')

    # Get user's content counts
    user_projects = Project.objects.filter(created_by=request.user) if hasattr(Project, 'created_by') else Project.objects.all()
    user_skills = Skill.objects.all()  # Will be filtered by user later
    user_education = Education.objects.all()
    user_certifications = Certification.objects.all()
    user_services = Service.objects.all()

    context = {
        'title': 'Dashboard',
        'user_profile': user_profile,
        'projects_count': user_projects.count(),
        'skills_count': user_skills.count(),
        'education_count': user_education.count(),
        'certifications_count': user_certifications.count(),
        'services_count': user_services.count(),
        'recent_projects': user_projects[:5],
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_settings(request):
    """User profile settings page"""

    # Ensure user has a profile (create if doesn't exist)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user_profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=user_profile)

    context = {
        'title': 'Profile Settings',
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/profile_settings.html', context)

