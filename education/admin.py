"""
Education App Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Skill, Education, Certification


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin interface for Skills"""

    list_display = [
        'name', 'category', 'proficiency_bar', 'proficiency_level',
        'is_featured', 'is_active', 'order'
    ]
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'is_active', 'order']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Skill Information', {
            'fields': ('name', 'category', 'proficiency', 'description')
        }),
        ('Visual', {
            'fields': ('icon_class', 'color')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )

    actions = ['make_featured', 'remove_featured']

    def get_queryset(self, request):
        """Filter skills for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Auto-assign user if not set"""
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def proficiency_bar(self, obj):
        """Display proficiency as progress bar"""
        color_map = {
            'primary': '#0d6efd',
            'success': '#198754',
            'info': '#0dcaf0',
            'warning': '#ffc107',
            'danger': '#dc3545',
        }
        color = color_map.get(obj.color, '#198754')
        return format_html(
            '<div style="width:100px; background:#e9ecef; border-radius:3px;">'
            '<div style="width:{}%; height:20px; background:{}; border-radius:3px; text-align:center; color:white; font-size:11px; line-height:20px;">{}</div>'
            '</div>',
            obj.proficiency, color, f'{obj.proficiency}%'
        )
    proficiency_bar.short_description = 'Proficiency'

    def proficiency_level(self, obj):
        """Show proficiency level label"""
        return obj.get_proficiency_label()
    proficiency_level.short_description = 'Level'

    def make_featured(self, request, queryset):
        """Mark skills as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} skill(s) marked as featured.')
    make_featured.short_description = 'Mark as featured'

    def remove_featured(self, request, queryset):
        """Remove featured status"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} skill(s) removed from featured.')
    remove_featured.short_description = 'Remove featured status'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Admin interface for Education"""

    list_display = [
        'institution', 'degree', 'field_of_study', 'date_range',
        'is_current', 'is_active', 'order'
    ]
    list_filter = ['degree', 'is_current', 'is_active', 'start_date']
    search_fields = ['institution', 'field_of_study', 'description']
    list_editable = ['is_active', 'order']
    date_hierarchy = 'start_date'

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Education Details', {
            'fields': ('institution', 'degree', 'field_of_study', 'description')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Information', {
            'fields': ('gpa', 'location', 'logo')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )

    def get_queryset(self, request):
        """Filter education for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Auto-assign user if not set"""
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def date_range(self, obj):
        """Display date range"""
        if obj.is_current:
            return format_html(
                '{} - <strong>Present</strong>',
                obj.start_date.strftime('%b %Y')
            )
        elif obj.end_date:
            return f"{obj.start_date.strftime('%b %Y')} - {obj.end_date.strftime('%b %Y')}"
        return obj.start_date.strftime('%b %Y')
    date_range.short_description = 'Duration'


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    """Admin interface for Certifications"""

    list_display = [
        'name', 'user', 'issuing_organization', 'issue_date', 'expiry_status',
        'credential_link', 'is_active', 'order'
    ]
    list_filter = ['user', 'issuing_organization', 'is_active', 'issue_date']
    search_fields = ['name', 'issuing_organization', 'credential_id', 'description', 'user__username']
    list_editable = ['is_active', 'order']
    date_hierarchy = 'issue_date'
    readonly_fields = ['expiry_status_detail']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Certification Details', {
            'fields': ('name', 'issuing_organization', 'description')
        }),
        ('Credential Information', {
            'fields': ('credential_id', 'credential_url', 'logo')
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiry_date', 'expiry_status_detail')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )

    def get_queryset(self, request):
        """Filter certifications for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Auto-assign user if not set"""
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def expiry_status(self, obj):
        """Show expiry status with color"""
        if not obj.expiry_date:
            return format_html('<span style="color: green;">No Expiry</span>')
        elif obj.is_expired:
            return format_html('<span style="color: red;">Expired</span>')
        else:
            return format_html('<span style="color: green;">Valid</span>')
    expiry_status.short_description = 'Status'

    def expiry_status_detail(self, obj):
        """Detailed expiry status"""
        if not obj.expiry_date:
            return "This certification does not expire"
        elif obj.is_expired:
            return format_html(
                '<span style="color: red; font-weight: bold;">Expired on {}</span>',
                obj.expiry_date.strftime('%B %d, %Y')
            )
        else:
            from datetime import date
            days_left = (obj.expiry_date - date.today()).days
            return format_html(
                '<span style="color: green;">Valid until {} ({} days remaining)</span>',
                obj.expiry_date.strftime('%B %d, %Y'),
                days_left
            )
    expiry_status_detail.short_description = 'Expiry Status'

    def credential_link(self, obj):
        """Display credential URL as link"""
        if obj.credential_url:
            return format_html(
                '<a href="{}" target="_blank">View Credential</a>',
                obj.credential_url
            )
        return '-'
    credential_link.short_description = 'Credential'


