"""
Services App Views
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Service, ServiceInquiry


def services_pro(request):
    """Services page view"""

    services = Service.objects.filter(is_active=True)
    featured_services = services.filter(is_featured=True)

    context = {
        'services': services,
        'featured_services': featured_services,
        'p': 'Services',
        'services_active': 'active',
    }

    return render(request, 'serve/serve.html', context)


class ServiceListView(ListView):
    """List all services"""
    model = Service
    template_name = 'serve/services_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ServiceDetailView(DetailView):
    """Service detail view"""
    model = Service
    template_name = 'serve/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

