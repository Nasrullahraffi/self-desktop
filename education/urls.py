"""
Education App URLs
"""

from django.urls import path
from . import views
from .views import SkillCreateView, SkillUpdateView, SkillDeleteView,EducationCreateView, EducationUpdateView, EducationDeleteView,CertificationCreateView, CertificationUpdateView, CertificationDeleteView



urlpatterns = [
    # Skills List
    path('', views.skills_pro, name='skills'),
    path('list/', views.SkillsListView.as_view(), name='skills_list'),

    # Skills CRUD
    path('skill/create/', SkillCreateView.as_view(), name='skill_create'),
    path('skill/<int:pk>/edit/', SkillUpdateView.as_view(), name='skill_edit'),
    path('skill/<int:pk>/delete/', SkillDeleteView.as_view(), name='skill_delete'),

    # Education CRUD
    path('education/create/', EducationCreateView.as_view(), name='education_create'),
    path('education/<int:pk>/edit/', EducationUpdateView.as_view(), name='education_edit'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education_delete'),

    # Certification CRUD
    path('certification/create/', CertificationCreateView.as_view(), name='certification_create'),
    path('certification/<int:pk>/edit/', CertificationUpdateView.as_view(), name='certification_edit'),
    path('certification/<int:pk>/delete/', CertificationDeleteView.as_view(), name='certification_delete'),
]
