"""
Core App Models
Handles portfolio profile, projects, social links, and testimonials
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse


class Profile(models.Model):
    """Main profile information - One per user"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio_profile', null=True, blank=True)

    full_name = models.CharField(max_length=200, help_text="Your full name")
    tagline = models.CharField(max_length=200, blank=True, help_text="Professional tagline/title")
    bio = models.TextField(blank=True, help_text="Short bio/about yourself")
    profile_picture = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        help_text="Professional profile photo"
    )
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        help_text="Upload your resume (PDF)"
    )

    # Contact Information
    email = models.EmailField(blank=True, help_text="Professional email")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone")
    location = models.CharField(max_length=200, blank=True, help_text="City, Country")

    # Professional Details
    years_experience = models.PositiveIntegerField(
        default=0,
        help_text="Years of professional experience"
    )
    projects_completed = models.PositiveIntegerField(
        default=0,
        help_text="Total projects completed"
    )
    happy_clients = models.PositiveIntegerField(
        default=0,
        help_text="Number of satisfied clients"
    )

    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Meta description for SEO"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Meta keywords, comma separated"
    )

    # Settings
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"


class Project(models.Model):
    """Portfolio Projects"""

    PROJECT_STATUS = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('planned', 'Planned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)

    title = models.CharField(max_length=200, help_text="Project title")
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(help_text="Project description")
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Short description for listings"
    )

    # Project Details
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/',
        blank=True,
        null=True,
        help_text="Project thumbnail image"
    )
    featured_image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        help_text="Main project image"
    )

    # Links
    github_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
        help_text="GitHub repository URL"
    )
    live_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
        help_text="Live project URL"
    )
    demo_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
        help_text="Demo/Video URL"
    )

    # Technologies
    technologies = models.CharField(
        max_length=500,
        help_text="Technologies used (comma separated)"
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=PROJECT_STATUS,
        default='completed'
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    # GitHub Integration
    github_repo_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="GitHub repository name (for auto-sync)"
    )
    github_stars = models.PositiveIntegerField(default=0, editable=False)
    github_forks = models.PositiveIntegerField(default=0, editable=False)
    github_language = models.CharField(max_length=50, blank=True, editable=False)

    # Display Settings
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower = first)"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['order', '-created_at']
        unique_together = [['user', 'slug']]

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(user=self.user, slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    def get_technologies_list(self):
        """Return technologies as a list"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class SocialLink(models.Model):
    """Social Media Links"""

    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('medium', 'Medium'),
        ('stackoverflow', 'Stack Overflow'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links', null=True, blank=True)

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(validators=[URLValidator()])
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="FontAwesome icon class (e.g., fab fa-github)"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
        ordering = ['order', 'platform']

    def __str__(self):
        return f"{self.user.username} - {self.get_platform_display()}"

    def save(self, *args, **kwargs):
        # Auto-set icon class based on platform
        if not self.icon_class:
            icon_map = {
                'github': 'fab fa-github',
                'linkedin': 'fab fa-linkedin',
                'twitter': 'fab fa-twitter',
                'facebook': 'fab fa-facebook',
                'instagram': 'fab fa-instagram',
                'youtube': 'fab fa-youtube',
                'medium': 'fab fa-medium',
                'stackoverflow': 'fab fa-stack-overflow',
            }
            self.icon_class = icon_map.get(self.platform, 'fas fa-link')
        return super().save(*args, **kwargs)


class Testimonial(models.Model):
    """Client/Colleague Testimonials"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials', null=True, blank=True)

    name = models.CharField(max_length=200, help_text="Person's name")
    position = models.CharField(max_length=200, help_text="Job title/position")
    company = models.CharField(max_length=200, blank=True, help_text="Company name")
    testimonial = models.TextField(help_text="Testimonial text")
    avatar = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Person's photo"
    )
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating out of 5"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.company} ({self.user.username})"


