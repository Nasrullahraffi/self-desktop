"""
Project Management Forms
"""

from django import forms
from core.models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating/editing projects with image upload"""

    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'description', 'short_description',
            'technologies', 'github_url', 'live_url', 'demo_url',
            'featured_image', 'status', 'is_featured', 'is_active',
            'start_date', 'end_date', 'order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'auto-generated-slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Detailed project description'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary for cards'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, React (comma separated)'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username/repo'}),
            'live_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'demo_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/watch?v=...'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }
        help_texts = {
            'slug': 'Leave blank to auto-generate from title',
            'technologies': 'Enter comma-separated values',
            'featured_image': 'Upload project screenshot or logo',
            'is_featured': 'Show on homepage',
        }

    def clean_slug(self):
        """Auto-generate slug if not provided"""
        slug = self.cleaned_data.get('slug')
        if not slug:
            from django.utils.text import slugify
            title = self.cleaned_data.get('title', '')
            slug = slugify(title)
        return slug

