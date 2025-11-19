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

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]

