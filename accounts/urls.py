"""
Accounts App URLs
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    # User Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Profile Settings
    path('settings/', views.profile_settings, name='profile_settings'),
]

