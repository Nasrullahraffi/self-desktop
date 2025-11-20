"""
Core App URLs
"""

from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.home_page, name='home'),

    # About
    path('about/', views.about_page, name='about'),

    # Profile
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),

    # Projects - List & Detail
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),

    # Projects - CRUD
    path('project/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/<slug:slug>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
