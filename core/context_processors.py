"""
Core App Context Processors
Add global context variables to all templates
"""

from django.conf import settings
from .models import Profile, SocialLink


def site_settings(request):
    """Add site-wide settings to template context"""

    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
        'SOCIAL_MEDIA': settings.SOCIAL_MEDIA,
        'GITHUB_USERNAME': settings.GITHUB_USERNAME,
    }

    return context


def profile_context(request):
    """Add user-specific profile to all templates"""

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user, is_active=True).first()
        social_links = SocialLink.objects.filter(user=request.user, is_active=True)
    else:
        profile = None
        social_links = []

    return {
        'site_profile': profile,
        'social_links': social_links,
    }

