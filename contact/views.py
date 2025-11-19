"""
Contact App Views
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage, Newsletter
from .forms import ContactForm, NewsletterForm


def contact_pro(request):
    """Contact page view with form handling"""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message
            contact_message = form.save(commit=False)

            # Capture IP address and user agent
            contact_message.ip_address = get_client_ip(request)
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')

            contact_message.save()

            # Send email notification to admin
            try:
                send_notification_email(contact_message)
            except Exception as e:
                print(f"Email error: {e}")

            messages.success(
                request,
                'Thank you for your message! I will get back to you as soon as possible.'
            )
            return redirect('contactus')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'p': 'Contact',
        'contact_active': 'active',
    }

    return render(request, 'cont/contact.html', context)


def newsletter_subscribe(request):
    """Newsletter subscription view"""

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thank you for subscribing to our newsletter!'
            )
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'Please provide a valid email address.')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_notification_email(contact_message):
    """Send email notification to admin"""

    subject = f'New Contact Message: {contact_message.subject}'
    message = f"""
    New contact message received:
    
    From: {contact_message.name}
    Email: {contact_message.email}
    Phone: {contact_message.phone or 'Not provided'}
    Company: {contact_message.company or 'Not provided'}
    
    Subject: {contact_message.subject}
    
    Message:
    {contact_message.message}
    
    ---
    IP Address: {contact_message.ip_address}
    Received: {contact_message.created_at}
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=True,
    )


# Social media redirect views
class FacebookRedirectView(RedirectView):
    """Redirect to Facebook profile"""
    url = settings.SOCIAL_MEDIA.get('facebook', 'https://www.facebook.com')
    permanent = False


class InstagramRedirectView(RedirectView):
    """Redirect to Instagram profile"""
    url = settings.SOCIAL_MEDIA.get('instagram', 'https://www.instagram.com')
    permanent = False


class LinkedInRedirectView(RedirectView):
    """Redirect to LinkedIn profile"""
    url = settings.SOCIAL_MEDIA.get('linkedin', 'https://www.linkedin.com')
    permanent = False


class TwitterRedirectView(RedirectView):
    """Redirect to Twitter profile"""
    url = settings.SOCIAL_MEDIA.get('twitter', 'https://www.twitter.com')
    permanent = False


class GitHubRedirectView(RedirectView):
    """Redirect to GitHub profile"""
    url = settings.SOCIAL_MEDIA.get('github', 'https://www.github.com')
    permanent = False

