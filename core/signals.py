"""
Core App Signals
Automatically create user profile on user registration
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile when a new User is created"""
    if created:
        Profile.objects.create(
            user=instance,
            full_name=instance.get_full_name() or instance.username,
            email=instance.email
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile whenever the user is saved"""
    if hasattr(instance, 'portfolio_profile'):
        # Update profile email and full name if changed
        profile = instance.portfolio_profile
        if instance.email and not profile.email:
            profile.email = instance.email
        if instance.get_full_name() and not profile.full_name:
            profile.full_name = instance.get_full_name()
        profile.save()

