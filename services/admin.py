"""
Services App Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Service, ServiceInquiry


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for Services"""

    list_display = [
        'title', 'user', 'icon_preview', 'price_display', 'delivery_time',
        'is_featured', 'is_active', 'order', 'updated_at'
    ]
    list_filter = ['user', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'features', 'user__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_active', 'order']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Service Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Visual', {
            'fields': ('icon_class', 'color', 'image')
        }),
        ('Pricing', {
            'fields': ('price_starting', 'price_currency', 'pricing_model')
        }),
        ('Details', {
            'fields': ('features', 'delivery_time')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )

    actions = ['make_featured', 'remove_featured']

    def get_queryset(self, request):
        """Filter services for non-superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Auto-assign user if not set"""
        if not change and not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def icon_preview(self, obj):
        """Display icon"""
        return format_html('<i class="{}"></i> {}', obj.icon_class, obj.icon_class)
    icon_preview.short_description = 'Icon'

    def price_display(self, obj):
        """Display formatted price"""
        return obj.get_price_display()
    price_display.short_description = 'Price'

    def make_featured(self, request, queryset):
        """Mark services as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} service(s) marked as featured.')
    make_featured.short_description = 'Mark as featured'

    def remove_featured(self, request, queryset):
        """Remove featured status"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} service(s) removed from featured.')
    remove_featured.short_description = 'Remove featured status'


@admin.register(ServiceInquiry)
class ServiceInquiryAdmin(admin.ModelAdmin):
    """Admin interface for Service Inquiries"""

    list_display = [
        'name', 'email', 'service', 'subject', 'status_badge',
        'budget', 'created_at'
    ]
    list_filter = ['status', 'service', 'created_at']
    search_fields = ['name', 'email', 'company', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Inquiry Details', {
            'fields': ('service', 'subject', 'message', 'budget', 'timeline')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_contacted', 'mark_as_in_progress', 'mark_as_completed']

    def status_badge(self, obj):
        """Display status with color"""
        colors = {
            'new': '#dc3545',
            'contacted': '#0dcaf0',
            'in_progress': '#ffc107',
            'completed': '#198754',
            'cancelled': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{}; color:white; padding:3px 8px; border-radius:3px; font-size:11px;">{}</span>',
            color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'

    def mark_as_contacted(self, request, queryset):
        """Mark inquiries as contacted"""
        updated = queryset.update(status='contacted')
        self.message_user(request, f'{updated} inquiry(ies) marked as contacted.')
    mark_as_contacted.short_description = 'Mark as contacted'

    def mark_as_in_progress(self, request, queryset):
        """Mark inquiries as in progress"""
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} inquiry(ies) marked as in progress.')
    mark_as_in_progress.short_description = 'Mark as in progress'

    def mark_as_completed(self, request, queryset):
        """Mark inquiries as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} inquiry(ies) marked as completed.')
    mark_as_completed.short_description = 'Mark as completed'

