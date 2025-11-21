"""
Management command to create a test user with sample data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Project, SocialLink
from education.models import Skill
from services.models import Service


class Command(BaseCommand):
    help = 'Creates a test user with sample portfolio data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='Email for the test user'
        )
        parser.add_argument(
            '--username',
            type=str,
            default='testuser',
            help='Username for the test user'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='testpass123',
            help='Password for the test user'
        )

    def handle(self, *args, **options):
        email = options['email']
        username = options['username']
        password = options['password']

        # Create or get user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'Test',
                'last_name': 'User'
            }
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))

        # Create or update profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'full_name': f'{user.first_name} {user.last_name}',
                'tagline': 'Full Stack Developer | Python Specialist',
                'bio': 'Passionate developer with expertise in Python, Django, and web technologies.',
                'email': user.email,
                'years_experience': 5,
                'projects_completed': 20,
                'happy_clients': 15
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created profile'))
        else:
            self.stdout.write(self.style.WARNING('Profile already exists'))

        # Create sample project if none exist
        if not Project.objects.filter(user=user).exists():
            Project.objects.create(
                user=user,
                title='Sample Portfolio Website',
                description='A modern, responsive portfolio website built with Django',
                short_description='Portfolio website with Django',
                technologies='Python, Django, HTML, CSS, JavaScript',
                status='completed',
                is_featured=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Created sample project'))

        # Create sample skills if none exist
        if not Skill.objects.filter(user=user).exists():
            skills_data = [
                {'name': 'Python', 'category': 'backend', 'proficiency': 90},
                {'name': 'Django', 'category': 'backend', 'proficiency': 85},
                {'name': 'JavaScript', 'category': 'frontend', 'proficiency': 75},
                {'name': 'HTML/CSS', 'category': 'frontend', 'proficiency': 80},
            ]

            for skill_data in skills_data:
                Skill.objects.create(user=user, **skill_data)

            self.stdout.write(self.style.SUCCESS(f'Created {len(skills_data)} sample skills'))

        # Create sample social links if none exist
        if not SocialLink.objects.filter(user=user).exists():
            SocialLink.objects.create(
                user=user,
                platform='github',
                url='https://github.com/testuser',
                is_active=True
            )
            SocialLink.objects.create(
                user=user,
                platform='linkedin',
                url='https://linkedin.com/in/testuser',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Created sample social links'))

        # Create sample service if none exist
        if not Service.objects.filter(user=user).exists():
            Service.objects.create(
                user=user,
                title='Web Development',
                short_description='Custom web application development',
                description='Full-stack web development services using modern technologies',
                is_featured=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Created sample service'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Test user setup complete!'))
        self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
        self.stdout.write(self.style.SUCCESS(f'\nYou can now log in at /accounts/login/'))

