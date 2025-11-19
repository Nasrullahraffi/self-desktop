"""
Services App Models
Handles services offered, pricing, and features
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Service(models.Model):
    """Services offered"""

    title = models.CharField(max_length=200, help_text="Service title")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(
        max_length=200,
        help_text="Brief description for cards"
    )
    description = models.TextField(help_text="Detailed service description")

    # Visual
    icon_class = models.CharField(
        max_length=100,
        default='fas fa-code',
        help_text="FontAwesome icon class (e.g., fas fa-code)"
    )
    color = models.CharField(
        max_length=20,
        default='primary',
        help_text="Bootstrap color class"
    )
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        help_text="Service image/illustration"
    )

    # Pricing
    price_starting = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Starting price (optional)"
    )
    price_currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (USD, EUR, etc.)"
    )
    pricing_model = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., 'per hour', 'per project', 'monthly'"
    )

    # Features (comma-separated or one per line)
    features = models.TextField(
        blank=True,
        help_text="Service features/highlights (one per line or comma-separated)"
    )

    # Delivery
    delivery_time = models.CharField(
        max_length=100,
        blank=True,
        help_text="Typical delivery time (e.g., '2-3 weeks')"
    )

    # Display Settings
    is_featured = models.BooleanField(
        default=False,
        help_text="Show prominently on homepage"
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
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

    def get_features_list(self):
        """Return features as a list"""
        if not self.features:
            return []
        # Support both newline and comma separation
        if '\n' in self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return [f.strip() for f in self.features.split(',') if f.strip()]

    def get_price_display(self):
        """Return formatted price"""
        if self.price_starting:
            price_str = f"{self.price_currency} {self.price_starting:,.2f}"
            if self.pricing_model:
                price_str += f" {self.pricing_model}"
            return price_str
        return "Contact for pricing"


class ServiceInquiry(models.Model):
    """Service inquiry/contact requests"""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inquiries'
    )

    # Contact Info
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)

    # Inquiry Details
    subject = models.CharField(max_length=200)
    message = models.TextField()
    budget = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    notes = models.TextField(blank=True, help_text="Internal notes")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Inquiry"
        verbose_name_plural = "Service Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"


