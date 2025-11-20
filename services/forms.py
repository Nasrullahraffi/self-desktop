"""
Services App Forms
"""

from django import forms
from services.models import Service


class ServiceForm(forms.ModelForm):
    """Form for creating/editing services"""

    class Meta:
        model = Service
        fields = [
            'title', 'slug', 'short_description', 'description',
            'icon_class', 'color', 'image', 'price_starting',
            'price_currency', 'pricing_model', 'features',
            'delivery_time', 'is_featured', 'is_active', 'order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Web Development, SEO Services'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'auto-generated-slug'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Brief one-liner for service cards'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Detailed service description with benefits'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-code, fas fa-chart-line, fas fa-mobile-alt'
            }),
            'color': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('primary', 'Primary (Blue)'),
                ('success', 'Success (Green)'),
                ('warning', 'Warning (Orange)'),
                ('danger', 'Danger (Red)'),
                ('info', 'Info (Cyan)'),
                ('secondary', 'Secondary (Gray)'),
            ]),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'price_starting': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '499.99'
            }),
            'price_currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'USD, EUR, GBP'
            }),
            'pricing_model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'per hour, per project, monthly'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Feature 1\nFeature 2\nFeature 3\n(One per line)'
            }),
            'delivery_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2-3 weeks, 5 business days'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
        }
        help_texts = {
            'slug': 'Leave blank to auto-generate from title',
            'icon_class': 'FontAwesome icon class for visual representation',
            'image': 'Optional service illustration or icon',
            'features': 'Enter one feature per line',
            'is_featured': 'Display prominently on homepage',
        }

    def clean_slug(self):
        """Auto-generate slug if not provided"""
        slug = self.cleaned_data.get('slug')
        if not slug:
            from django.utils.text import slugify
            title = self.cleaned_data.get('title', '')
            slug = slugify(title)
        return slug

    def clean_features(self):
        """Clean and format features"""
        features = self.cleaned_data.get('features', '')
        if features:
            # Split by newlines and remove empty lines
            features_list = [f.strip() for f in features.split('\n') if f.strip()]
            # Join back with newlines
            return '\n'.join(features_list)
        return features

