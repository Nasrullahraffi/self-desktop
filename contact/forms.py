"""
Contact App Forms
"""

from django import forms
from django.core.validators import validate_email
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import ContactMessage, Newsletter


class ContactForm(forms.ModelForm):
    """Contact form with validation"""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567 (Optional)',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name (Optional)',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your message',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here...',
                'rows': 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-3'),
                Column('company', css_class='form-group col-md-6 mb-3'),
            ),
            Field('subject', css_class='form-group mb-3'),
            Field('message', css_class='form-group mb-3'),
            Submit('submit', 'Send Message', css_class='btn btn-primary btn-lg')
        )

    def clean_email(self):
        """Validate email"""
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email.lower()

    def clean_message(self):
        """Validate message length"""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        return message


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""

    class Meta:
        model = Newsletter
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (Optional)',
            }),
        }

    def clean_email(self):
        """Validate and check if email already subscribed"""
        email = self.cleaned_data.get('email')
        validate_email(email)
        email = email.lower()

        # Check if already subscribed
        if Newsletter.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('This email is already subscribed to our newsletter.')

        return email

