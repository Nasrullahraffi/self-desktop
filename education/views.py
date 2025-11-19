"""
Education App Views
"""

from django.shortcuts import render
from django.views.generic import ListView
from .models import Skill, Education, Certification


def skills_pro(request):
    """Skills page view"""

    # Get skills by category
    skills = Skill.objects.filter(is_active=True)

    # Group skills by category
    frontend_skills = skills.filter(category='frontend')
    backend_skills = skills.filter(category='backend')
    database_skills = skills.filter(category='database')
    devops_skills = skills.filter(category='devops')
    design_skills = skills.filter(category='design')
    soft_skills = skills.filter(category='soft')
    other_skills = skills.filter(category='other')

    # Get education
    education = Education.objects.filter(is_active=True)

    # Get certifications
    certifications = Certification.objects.filter(is_active=True)

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


class SkillsListView(ListView):
    """Alternative class-based view for skills"""
    model = Skill
    template_name = 'skills/skills_list.html'
    context_object_name = 'skills'

    def get_queryset(self):
        return Skill.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['education'] = Education.objects.filter(is_active=True)
        context['certifications'] = Certification.objects.filter(is_active=True)
        return context

