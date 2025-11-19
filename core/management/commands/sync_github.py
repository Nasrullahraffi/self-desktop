"""
Management command to sync GitHub repositories
Usage: python manage.py sync_github
"""

from django.core.management.base import BaseCommand
from core.github_utils import sync_github_projects


class Command(BaseCommand):
    help = 'Sync GitHub repositories to projects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--activate',
            action='store_true',
            help='Automatically activate synced projects',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Syncing GitHub repositories...'))

        try:
            from core.github_utils import GitHubAPI
            api = GitHubAPI()
            projects = api.sync_all_repos(auto_activate=options.get('activate', False))

            self.stdout.write(
                self.style.SUCCESS(f'Successfully synced {len(projects)} projects from GitHub')
            )

            for project in projects:
                status = '✓ Active' if project.is_active else '○ Inactive'
                stars = f'⭐ {project.github_stars}' if project.github_stars else ''
                self.stdout.write(f'  {status} {project.title} {stars}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error syncing GitHub projects: {str(e)}')
            )

