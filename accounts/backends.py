"""
Custom Authentication Backends
Allows users to authenticate with email instead of username
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrUsernameBackend(ModelBackend):
    """
    Authenticate using email or username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to fetch the user by searching the username or email field
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user
            User().set_password(password)
        except User.MultipleObjectsReturned:
            # If there are multiple users with the same email, use the first one
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
            if user and user.check_password(password):
                return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

