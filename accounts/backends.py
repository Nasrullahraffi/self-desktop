"""
Custom Authentication Backend
Allows users to authenticate with email (primary) or username (fallback)
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailOrUsernameBackend(ModelBackend):
    """
    Authenticate using email (primary) or username (fallback)
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by email or username
        Args:
            username: Can be either email or username
            password: User password
        """
        if username is None or password is None:
            return None

        try:
            # Try to find user by email first
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                # Fallback to username for backward compatibility
                user = User.objects.get(username__iexact=username)

            # Verify password and check if user is active
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        except User.DoesNotExist:
            # Run the default password hasher to reduce timing difference
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # If multiple users with same email, return None for security
            return None

        return None

    def get_user(self, user_id):
        """Get user by ID"""
        try:
            user = User.objects.get(pk=user_id)
            return user if self.user_can_authenticate(user) else None
        except User.DoesNotExist:
            return None
            return None

