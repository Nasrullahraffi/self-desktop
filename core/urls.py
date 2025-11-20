"""
Core App URLs
"""

from django.urls import path
from . import views
from .views import ProjectCreateView, ProjectUpdateView, ProjectDeleteView, ProjectListView, ProjectDetailView

urlpatterns = [
    # Homepage
    path('', views.home_page, name='home'),

    # About
    path('about/', views.about_page, name='about'),

    # Profile
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),

    # Projects - List
    path('projects/', ProjectListView.as_view(), name='projects'),

    # Projects - CRUD (create/edit/delete MUST come before detail with slug)
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<slug:slug>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<slug:slug>/delete/', ProjectDeleteView.as_view(), name='project_delete'),

    # Project Detail (MUST be last to avoid matching 'create', 'edit', 'delete' as slugs)
    path('project/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]
