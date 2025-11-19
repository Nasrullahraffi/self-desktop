"""
Core App Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Project, SocialLink, Testimonial


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for Profile"""

    list_display = ['full_name', 'tagline', 'email', 'years_experience', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['full_name', 'email', 'bio']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'tagline', 'bio', 'profile_picture', 'resume')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Professional Stats', {
            'fields': ('years_experience', 'projects_completed', 'happy_clients')
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    def has_add_permission(self, request):
        """Only allow one profile instance"""
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for Projects"""

    list_display = [
        'title', 'status', 'is_featured', 'github_stars_display',
        'technologies_preview', 'is_active', 'order', 'updated_at'
    ]
    list_filter = ['status', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'technologies', 'github_repo_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['github_stars', 'github_forks', 'github_language', 'created_at', 'updated_at']
    list_editable = ['order', 'is_featured', 'is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'status')
        }),
        ('Media', {
            'fields': ('thumbnail', 'featured_image')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url', 'demo_url')
        }),
        ('Technical Details', {
            'fields': ('technologies', 'start_date', 'end_date')
        }),
        ('GitHub Integration', {
            'fields': ('github_repo_name', 'github_stars', 'github_forks', 'github_language'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['make_featured', 'remove_featured', 'activate_projects', 'deactivate_projects']

    def github_stars_display(self, obj):
        """Display GitHub stars with icon"""
        if obj.github_stars:
            return format_html('⭐ {}', obj.github_stars)
        return '-'
    github_stars_display.short_description = 'Stars'

    def technologies_preview(self, obj):
        """Show first 3 technologies"""
        techs = obj.get_technologies_list()[:3]
        preview = ', '.join(techs)
        if len(obj.get_technologies_list()) > 3:
            preview += '...'
        return preview
    technologies_preview.short_description = 'Technologies'

    def make_featured(self, request, queryset):
        """Mark projects as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} project(s) marked as featured.')
    make_featured.short_description = 'Mark as featured'

    def remove_featured(self, request, queryset):
        """Remove featured status"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} project(s) removed from featured.')
    remove_featured.short_description = 'Remove featured status'

    def activate_projects(self, request, queryset):
        """Activate selected projects"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} project(s) activated.')
    activate_projects.short_description = 'Activate selected projects'

    def deactivate_projects(self, request, queryset):
        """Deactivate selected projects"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} project(s) deactivated.')
    deactivate_projects.short_description = 'Deactivate selected projects'


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """Admin interface for Social Links"""

    list_display = ['platform', 'url_preview', 'icon_class', 'is_active', 'order']
    list_filter = ['platform', 'is_active']
    search_fields = ['platform', 'url']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'platform']

    fieldsets = (
        ('Social Link', {
            'fields': ('platform', 'url', 'icon_class')
        }),
        ('Display', {
            'fields': ('is_active', 'order')
        }),
    )

    def url_preview(self, obj):
        """Show clickable URL"""
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url[:50])
    url_preview.short_description = 'URL'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin interface for Testimonials"""

    list_display = ['name', 'position', 'company', 'rating_display', 'is_active', 'order', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'company', 'position', 'testimonial']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Person Information', {
            'fields': ('name', 'position', 'company', 'avatar')
        }),
        ('Testimonial', {
            'fields': ('testimonial', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order', 'created_at')
        }),
    )

    def rating_display(self, obj):
        """Display rating as stars"""
        stars = '⭐' * obj.rating
        return format_html('{} ({})', stars, obj.rating)
    rating_display.short_description = 'Rating'


# Customize admin site header
admin.site.site_header = "Portfolio Admin Panel"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"


