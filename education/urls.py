"""
Education App URLs
"""

from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    path('', views.skills_pro, name='skills'),
    path('list/', views.SkillsListView.as_view(), name='skills_list'),
]


