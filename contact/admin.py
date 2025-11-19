"""
Contact App Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import ContactMessage, Newsletter


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for Contact Messages"""

    list_display = [
        'name', 'email', 'subject', 'status_badge', 'priority_badge',
        'age_display', 'created_at'
    ]
    list_filter = ['status', 'priority', 'created_at', 'read_at']
    search_fields = ['name', 'email', 'company', 'subject', 'message']
    readonly_fields = [
        'ip_address', 'user_agent', 'created_at', 'updated_at',
        'read_at', 'replied_at', 'age_display_detail'
    ]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status Management', {
            'fields': ('status', 'priority', 'admin_notes')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': (
                'created_at', 'updated_at', 'read_at',
                'replied_at', 'age_display_detail'
            ),
            'classes': ('collapse',)
        }),
    )

    actions = [
        'mark_as_read', 'mark_as_replied', 'mark_as_archived',
        'set_priority_high', 'set_priority_urgent'
    ]

    def status_badge(self, obj):
        """Display status with color"""
        colors = {
            'new': '#dc3545',
            'read': '#0dcaf0',
            'replied': '#198754',
            'archived': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        badge_icon = '🔴' if obj.status == 'new' else '✓'
        return format_html(
            '{} <span style="background:{}; color:white; padding:3px 8px; border-radius:3px; font-size:11px;">{}</span>',
            badge_icon, color, obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'

    def priority_badge(self, obj):
        """Display priority with color"""
        colors = {
            'low': '#6c757d',
            'normal': '#0dcaf0',
            'high': '#ffc107',
            'urgent': '#dc3545',
        }
        color = colors.get(obj.priority, '#0dcaf0')
        return format_html(
            '<span style="background:{}; color:white; padding:3px 8px; border-radius:3px; font-size:11px;">{}</span>',
            color, obj.get_priority_display().upper()
        )
    priority_badge.short_description = 'Priority'

    def age_display(self, obj):
        """Display message age"""
        days = obj.age_in_days
        if days == 0:
            return 'Today'
        elif days == 1:
            return 'Yesterday'
        elif days < 7:
            return f'{days} days ago'
        elif days < 30:
            weeks = days // 7
            return f'{weeks} week{"s" if weeks > 1 else ""} ago'
        else:
            months = days // 30
            return f'{months} month{"s" if months > 1 else ""} ago'
    age_display.short_description = 'Age'

    def age_display_detail(self, obj):
        """Detailed age information"""
        return f"{obj.age_in_days} days old"
    age_display_detail.short_description = 'Message Age'

    # Admin actions
    def mark_as_read(self, request, queryset):
        """Mark messages as read"""
        for msg in queryset:
            if msg.status == 'new':
                msg.mark_as_read()
        self.message_user(request, f'{queryset.count()} message(s) marked as read.')
    mark_as_read.short_description = 'Mark as read'

    def mark_as_replied(self, request, queryset):
        """Mark messages as replied"""
        for msg in queryset:
            msg.mark_as_replied()
        self.message_user(request, f'{queryset.count()} message(s) marked as replied.')
    mark_as_replied.short_description = 'Mark as replied'

    def mark_as_archived(self, request, queryset):
        """Archive messages"""
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} message(s) archived.')
    mark_as_archived.short_description = 'Archive messages'

    def set_priority_high(self, request, queryset):
        """Set priority to high"""
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} message(s) set to high priority.')
    set_priority_high.short_description = 'Set priority: High'

    def set_priority_urgent(self, request, queryset):
        """Set priority to urgent"""
        updated = queryset.update(priority='urgent')
        self.message_user(request, f'{updated} message(s) set to urgent priority.')
    set_priority_urgent.short_description = 'Set priority: Urgent'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin interface for Newsletter Subscriptions"""

    list_display = [
        'email', 'name', 'subscription_status', 'frequency',
        'verified_badge', 'subscribed_at'
    ]
    list_filter = ['is_active', 'is_verified', 'frequency', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at', 'verification_token']
    date_hierarchy = 'subscribed_at'

    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'name')
        }),
        ('Subscription Settings', {
            'fields': ('is_active', 'is_verified', 'frequency')
        }),
        ('Metadata', {
            'fields': ('subscribed_at', 'unsubscribed_at', 'verification_token'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_subscriptions', 'deactivate_subscriptions', 'mark_as_verified']

    def subscription_status(self, obj):
        """Display subscription status"""
        if obj.is_active:
            return format_html(
                '<span style="color: green;">● Active</span>'
            )
        return format_html(
            '<span style="color: red;">● Inactive</span>'
        )
    subscription_status.short_description = 'Status'

    def verified_badge(self, obj):
        """Display verification status"""
        if obj.is_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        return format_html('<span style="color: orange;">⚠ Not Verified</span>')
    verified_badge.short_description = 'Verified'

    def activate_subscriptions(self, request, queryset):
        """Activate subscriptions"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscription(s) activated.')
    activate_subscriptions.short_description = 'Activate selected subscriptions'

    def deactivate_subscriptions(self, request, queryset):
        """Deactivate subscriptions"""
        for sub in queryset:
            sub.unsubscribe()
        self.message_user(request, f'{queryset.count()} subscription(s) deactivated.')
    deactivate_subscriptions.short_description = 'Deactivate selected subscriptions'

    def mark_as_verified(self, request, queryset):
        """Mark as verified"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} subscription(s) marked as verified.')
    mark_as_verified.short_description = 'Mark as verified'


