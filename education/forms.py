"""
Skill Management Forms
"""

from django import forms
from education.models import Skill, Education, Certification


class SkillForm(forms.ModelForm):
    """Form for creating/editing skills"""

    class Meta:
        model = Skill
        fields = [
            'name', 'category', 'proficiency', 'icon_class',
            'description', 'is_active', 'order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Python, React, PostgreSQL'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'proficiency': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'placeholder': '0-100'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fab fa-python (FontAwesome class)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of your experience'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
        }
        help_texts = {
            'proficiency': 'Rate your proficiency from 0-100%',
            'icon_class': 'Optional FontAwesome icon class',
        }


class EducationForm(forms.ModelForm):
    """Form for creating/editing education records"""

    class Meta:
        model = Education
        fields = [
            'institution', 'degree', 'field_of_study', 'start_date',
            'end_date', 'is_current', 'gpa', 'description',
            'location', 'is_active', 'order'
        ]
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'University/College name'
            }),
            'degree': forms.Select(attrs={'class': 'form-select'}),
            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Computer Science, Engineering, etc.'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'max': 4,
                'placeholder': '0.00'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Achievements, coursework, etc.'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
        }


class CertificationForm(forms.ModelForm):
    """Form for creating/editing certifications"""

    class Meta:
        model = Certification
        fields = [
            'name', 'issuing_organization', 'issue_date', 'expiry_date',
            'credential_id', 'credential_url', 'description', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certification name'
            }),
            'issuing_organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'AWS, Google, Microsoft, etc.'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'credential_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certificate ID (optional)'
            }),
            'credential_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://verify.example.com'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

