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
    """Add profile to all templates"""

    profile = Profile.objects.filter(is_active=True).first()
    social_links = SocialLink.objects.filter(is_active=True)

    return {
        'site_profile': profile,
        'social_links': social_links,
    }

