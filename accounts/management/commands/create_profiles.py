"""
Management command to create UserProfiles for users who don't have one
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Creates UserProfile for all users who do not have one'

    def handle(self, *args, **options):
        users_without_profile = []

        for user in User.objects.all():
            if not hasattr(user, 'user_profile'):
                users_without_profile.append(user)

        if not users_without_profile:
            self.stdout.write(self.style.SUCCESS('✅ All users already have profiles!'))
            return

        self.stdout.write(f'Found {len(users_without_profile)} user(s) without profiles.')

        created_count = 0
        for user in users_without_profile:
            try:
                UserProfile.objects.create(user=user)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Created profile for: {user.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Failed to create profile for {user.username}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Created {created_count} profile(s)!'))

