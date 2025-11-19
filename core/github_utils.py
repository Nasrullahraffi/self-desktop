"""
GitHub Integration Utilities
Fetch and sync GitHub repositories
"""

import requests
from django.conf import settings
from core.models import Project


class GitHubAPI:
    """GitHub API integration"""

    BASE_URL = 'https://api.github.com'

    def __init__(self):
        self.username = settings.GITHUB_USERNAME
        self.token = settings.GITHUB_TOKEN
        self.headers = {}

        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

    def get_user_repos(self, sort='updated', per_page=100):
        """Get all user repositories"""

        if not self.username:
            return []

        url = f'{self.BASE_URL}/users/{self.username}/repos'
        params = {
            'sort': sort,
            'per_page': per_page,
            'type': 'owner'
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching GitHub repos: {e}")
            return []

    def get_repo_details(self, repo_name):
        """Get detailed information about a repository"""

        if not self.username:
            return None

        url = f'{self.BASE_URL}/repos/{self.username}/{repo_name}'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching repo details: {e}")
            return None

    def get_repo_languages(self, repo_name):
        """Get programming languages used in a repository"""

        if not self.username:
            return {}

        url = f'{self.BASE_URL}/repos/{self.username}/{repo_name}/languages'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching repo languages: {e}")
            return {}

    def sync_repository_to_project(self, repo_data):
        """Sync a GitHub repository to a Project instance"""

        # Extract data
        repo_name = repo_data.get('name', '')
        description = repo_data.get('description', '')
        html_url = repo_data.get('html_url', '')
        homepage = repo_data.get('homepage', '')
        stars = repo_data.get('stargazers_count', 0)
        forks = repo_data.get('forks_count', 0)
        language = repo_data.get('language', '')
        topics = repo_data.get('topics', [])
        created_at = repo_data.get('created_at', '')
        updated_at = repo_data.get('updated_at', '')

        # Get or create project
        project, created = Project.objects.get_or_create(
            github_repo_name=repo_name,
            defaults={
                'title': repo_name.replace('-', ' ').replace('_', ' ').title(),
                'description': description or f"GitHub repository: {repo_name}",
                'short_description': description[:200] if description else '',
                'github_url': html_url,
                'live_url': homepage or '',
                'technologies': ', '.join(topics) if topics else language,
                'github_stars': stars,
                'github_forks': forks,
                'github_language': language,
                'status': 'completed',
            }
        )

        # Update if not created
        if not created:
            project.github_url = html_url
            project.live_url = homepage or project.live_url
            project.github_stars = stars
            project.github_forks = forks
            project.github_language = language

            # Update technologies if not manually set
            if not project.technologies or project.technologies == language:
                project.technologies = ', '.join(topics) if topics else language

            project.save()

        return project

    def sync_all_repos(self, auto_activate=False):
        """Sync all GitHub repositories to projects"""

        repos = self.get_user_repos()
        synced_projects = []

        for repo in repos:
            # Skip forks if desired
            if repo.get('fork', False):
                continue

            project = self.sync_repository_to_project(repo)

            if auto_activate and not project.is_active:
                project.is_active = True
                project.save()

            synced_projects.append(project)

        return synced_projects


def sync_github_projects():
    """Convenience function to sync GitHub projects"""

    if not settings.GITHUB_USERNAME:
        print("GitHub username not configured")
        return []

    api = GitHubAPI()
    projects = api.sync_all_repos(auto_activate=False)

    print(f"Synced {len(projects)} projects from GitHub")
    return projects

