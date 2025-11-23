"""
Education App Views
"""

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Skill, Education, Certification
from .forms import SkillForm, EducationForm, CertificationForm


def skills_pro(request):
    """Skills page view"""

    if request.user.is_authenticated:
        # Get user's skills by category
        skills = Skill.objects.filter(user=request.user, is_active=True)

        # Group skills by category
        frontend_skills = skills.filter(category='frontend')
        backend_skills = skills.filter(category='backend')
        database_skills = skills.filter(category='database')
        devops_skills = skills.filter(category='devops')
        design_skills = skills.filter(category='design')
        soft_skills = skills.filter(category='soft')
        other_skills = skills.filter(category='other')

        # Get user's education
        education = Education.objects.filter(user=request.user, is_active=True)

        # Get user's certifications
        certifications = Certification.objects.filter(user=request.user, is_active=True)
    else:
        skills = []
        frontend_skills = []
        backend_skills = []
        database_skills = []
        devops_skills = []
        design_skills = []
        soft_skills = []
        other_skills = []
        education = []
        certifications = []

    context = {
        'skills': skills,
        'frontend_skills': frontend_skills,
        'backend_skills': backend_skills,
        'database_skills': database_skills,
        'devops_skills': devops_skills,
        'design_skills': design_skills,
        'soft_skills': soft_skills,
        'other_skills': other_skills,
        'education': education,
        'certifications': certifications,
        'p': 'Skills & Education',
        'skills_active': 'active',
    }

    return render(request, 'skills/skills.html', context)


class SkillsListView(LoginRequiredMixin, ListView):
    """Alternative class-based view for skills"""
    model = Skill
    template_name = 'skills/skills_list.html'
    context_object_name = 'skills'

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['education'] = Education.objects.filter(user=self.request.user, is_active=True)
        context['certifications'] = Certification.objects.filter(user=self.request.user, is_active=True)
        return context

# =============================================================================
# SKILL CRUD VIEWS
# ==============================================================================

class SkillCreateView(LoginRequiredMixin, CreateView):
    """Create new skill"""
    model = Skill
    form_class = SkillForm
    template_name = 'skills/skill_form.html'
    success_url = reverse_lazy('skills')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Skill added successfully!')
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing skill"""
    model = Skill
    form_class = SkillForm
    template_name = 'skills/skill_form.html'
    success_url = reverse_lazy('skills')

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Skill updated successfully!')
        return super().form_valid(form)


class SkillDeleteView(LoginRequiredMixin, DeleteView):
    """Delete skill"""
    model = Skill
    template_name = 'skills/skill_confirm_delete.html'
    success_url = reverse_lazy('skills')

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Skill deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# EDUCATION CRUD VIEWS
# ==============================================================================

class EducationCreateView(LoginRequiredMixin, CreateView):
    """Create new education record"""
    model = Education
    form_class = EducationForm
    template_name = 'skills/education_form.html'
    success_url = reverse_lazy('skills')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Education record added successfully!')
        return super().form_valid(form)


class EducationUpdateView(LoginRequiredMixin, UpdateView):
    """Update education record"""
    model = Education
    form_class = EducationForm
    template_name = 'skills/education_form.html'
    success_url = reverse_lazy('skills')

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Education record updated successfully!')
        return super().form_valid(form)


class EducationDeleteView(LoginRequiredMixin, DeleteView):
    """Delete education record"""
    model = Education
    template_name = 'skills/education_confirm_delete.html'
    success_url = reverse_lazy('skills')

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Education record deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# CERTIFICATION CRUD VIEWS
# ==============================================================================

class CertificationCreateView(LoginRequiredMixin, CreateView):
    """Create new certification"""
    model = Certification
    form_class = CertificationForm
    template_name = 'skills/certification_form.html'
    success_url = reverse_lazy('skills')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Certification added successfully!')
        return super().form_valid(form)


class CertificationUpdateView(LoginRequiredMixin, UpdateView):
    """Update certification"""
    model = Certification
    form_class = CertificationForm
    template_name = 'skills/certification_form.html'
    success_url = reverse_lazy('skills')

    def get_queryset(self):
        return Certification.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Certification updated successfully!')
        return super().form_valid(form)


class CertificationDeleteView(LoginRequiredMixin, DeleteView):
    """Delete certification"""
    model = Certification
    template_name = 'skills/certification_confirm_delete.html'
    success_url = reverse_lazy('skills')

    def get_queryset(self):
        return Certification.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Certification deleted successfully!')
        return super().delete(request, *args, **kwargs)
