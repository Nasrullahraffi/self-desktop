"""
Accounts App Models
Extends Django's User model for user authentication and profiles
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile linked to Django User"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')

    # Profile information
    bio = models.TextField(blank=True, help_text="Short bio")
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    # Profile picture
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile picture"
    )

    # Social links
    github_username = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_username = models.CharField(max_length=100, blank=True)

    # Settings
    is_profile_public = models.BooleanField(default=True, help_text="Make profile visible to others")
    email_notifications = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        """Get user's full name or username"""
        return self.user.get_full_name() or self.user.username

    @property
    def display_name(self):
        """Get display name (first name or username)"""
        return self.user.first_name or self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'user_profile'):
        instance.user_profile.save()

