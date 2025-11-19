"""
Contact App Models
Handles contact messages and inquiries
"""

from django.db import models
from django.core.validators import validate_email


class ContactMessage(models.Model):
    """Contact form submissions"""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Contact Information
    name = models.CharField(max_length=200, help_text="Sender's name")
    email = models.EmailField(validators=[validate_email], help_text="Sender's email")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone (optional)")
    company = models.CharField(max_length=200, blank=True, help_text="Company name (optional)")

    # Message Details
    subject = models.CharField(max_length=200, help_text="Message subject")
    message = models.TextField(help_text="Message content")

    # Metadata
    ip_address = models.GenericIPAddressField(blank=True, null=True, editable=False)
    user_agent = models.TextField(blank=True, editable=False)

    # Status Management
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Message status"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal',
        help_text="Message priority"
    )

    # Admin Notes
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes (not visible to sender)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"

    def mark_as_read(self):
        """Mark message as read"""
        if self.status == 'new':
            self.status = 'read'
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save(update_fields=['status', 'read_at'])

    def mark_as_replied(self):
        """Mark message as replied"""
        self.status = 'replied'
        from django.utils import timezone
        self.replied_at = timezone.now()
        self.save(update_fields=['status', 'replied_at'])

    @property
    def is_new(self):
        """Check if message is new"""
        return self.status == 'new'

    @property
    def age_in_days(self):
        """Get message age in days"""
        from django.utils import timezone
        delta = timezone.now() - self.created_at
        return delta.days


class Newsletter(models.Model):
    """Newsletter subscription"""

    email = models.EmailField(
        unique=True,
        validators=[validate_email],
        help_text="Subscriber email"
    )
    name = models.CharField(max_length=200, blank=True, help_text="Subscriber name")

    # Status
    is_active = models.BooleanField(default=True, help_text="Active subscription")
    is_verified = models.BooleanField(default=False, help_text="Email verified")

    # Preferences
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
        ],
        default='monthly',
        help_text="Email frequency preference"
    )

    # Metadata
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    verification_token = models.CharField(max_length=64, blank=True, editable=False)

    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.email} ({'Active' if self.is_active else 'Inactive'})"

    def unsubscribe(self):
        """Unsubscribe user"""
        self.is_active = False
        from django.utils import timezone
        self.unsubscribed_at = timezone.now()
        self.save(update_fields=['is_active', 'unsubscribed_at'])


