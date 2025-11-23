"""
Core App Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Project, SocialLink, Testimonial


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for Profile"""

    list_display = ['full_name', 'user', 'tagline', 'email', 'years_experience', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'user']
    search_fields = ['full_name', 'email', 'bio', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
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

    def get_queryset(self, request):
        """Filter profiles for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Auto-assign user if not set"""
        if not change and not obj.user:  # If creating new object and user not set
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for Projects"""

    list_display = [
        'title', 'user', 'status', 'is_featured', 'github_stars_display',
        'technologies_preview', 'is_active', 'order', 'updated_at'
    ]
    list_filter = ['user', 'status', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'technologies', 'github_repo_name', 'user__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['github_stars', 'github_forks', 'github_language', 'created_at', 'updated_at']
    list_editable = ['order', 'is_featured', 'is_active']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
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

    def get_queryset(self, request):
        """Filter projects for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Auto-assign user if not set"""
        if not change and not obj.user:  # If creating new object and user not set
            obj.user = request.user
        super().save_model(request, obj, form, change)

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

    list_display = ['platform', 'user', 'url_preview', 'icon_class', 'is_active', 'order']
    list_filter = ['user', 'platform', 'is_active']
    search_fields = ['platform', 'url', 'user__username']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'platform']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Social Link', {
            'fields': ('platform', 'url', 'icon_class')
        }),
        ('Display', {
            'fields': ('is_active', 'order')
        }),
    )

    def get_queryset(self, request):
        """Filter social links for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Auto-assign user if not set"""
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def url_preview(self, obj):
        """Show clickable URL"""
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url[:50])
    url_preview.short_description = 'URL'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin interface for Testimonials"""

    list_display = ['name', 'user', 'position', 'company', 'rating_display', 'is_active', 'order', 'created_at']
    list_filter = ['user', 'rating', 'is_active', 'created_at']
    search_fields = ['name', 'company', 'position', 'testimonial', 'user__username']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
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

    def get_queryset(self, request):
        """Filter testimonials for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Auto-assign user if not set"""
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def rating_display(self, obj):
        """Display rating as stars"""
        stars = '⭐' * obj.rating
        return format_html('{} ({})', stars, obj.rating)
    rating_display.short_description = 'Rating'


# Customize admin site header
admin.site.site_header = "Portfolio Admin Panel"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"


