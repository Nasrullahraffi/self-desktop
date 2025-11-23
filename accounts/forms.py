"""
Accounts App Forms
Registration, Login, and Profile Management Forms
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """User registration form with email (email is used for login)"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
            'autofocus': True
        }),
        help_text='Required. You will use this email to log in.'
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username field as we'll generate it from email
        if 'username' in self.fields:
            del self.fields['username']

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email.lower()

    def save(self, commit=True):
        """Generate username from email and save user"""
        user = super().save(commit=False)
        # Generate unique username from email
        email = self.cleaned_data['email']
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        user.email = email
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Custom login form with Bootstrap styling - authenticate using email"""

    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True
        }),
        help_text='Enter the email you used to register'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class UserUpdateForm(forms.ModelForm):
    """Form to update user information"""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserProfileUpdateForm(forms.ModelForm):
    """Form to update user profile"""

    class Meta:
        model = UserProfile
        fields = (
            'bio', 'phone', 'location', 'website', 'avatar',
            'github_username', 'linkedin_url', 'twitter_username',
            'is_profile_public', 'email_notifications'
        )
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/username'
            }),
            'twitter_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            'is_profile_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

