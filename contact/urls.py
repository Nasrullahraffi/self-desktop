"""
Contact App URLs
"""

from django.urls import path
from . import views

urlpatterns = [
    # Contact page
    path('', views.contact_pro, name='contactus'),

    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    # Social media redirects
    path('social/facebook/', views.FacebookRedirectView.as_view(), name='fb'),
    path('social/instagram/', views.InstagramRedirectView.as_view(), name='inst'),
    path('social/linkedin/', views.LinkedInRedirectView.as_view(), name='linkedin'),
    path('social/twitter/', views.TwitterRedirectView.as_view(), name='twitter'),
    path('social/github/', views.GitHubRedirectView.as_view(), name='github'),
]


