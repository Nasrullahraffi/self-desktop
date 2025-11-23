"""
Services App Views
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Service
from .forms import ServiceForm


def services_pro(request):
    """Services page view"""

    if request.user.is_authenticated:
        services = Service.objects.filter(user=request.user, is_active=True)
        featured_services = services.filter(is_featured=True)
    else:
        services = []
        featured_services = []

    context = {
        'services': services,
        'featured_services': featured_services,
        'p': 'Services',
        'services_active': 'active',
    }

    return render(request, 'serve/serve.html', context)


class ServiceListView(LoginRequiredMixin, ListView):
    """List all user's services"""
    model = Service
    template_name = 'serve/services_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user, is_active=True)


class ServiceDetailView(LoginRequiredMixin, DetailView):
    """Service detail view"""
    model = Service
    template_name = 'serve/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user, is_active=True)


# ==============================================================================
# SERVICE CRUD VIEWS
# ==============================================================================

class ServiceCreateView(LoginRequiredMixin, CreateView):
    """Create new service"""
    model = Service
    form_class = ServiceForm
    template_name = 'serve/service_form.html'
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Service created successfully!')
        return super().form_valid(form)


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing service"""
    model = Service
    form_class = ServiceForm
    template_name = 'serve/service_form.html'
    success_url = reverse_lazy('services')

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Service updated successfully!')
        return super().form_valid(form)


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    """Delete service"""
    model = Service
    template_name = 'serve/service_confirm_delete.html'
    success_url = reverse_lazy('services')

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Service deleted successfully!')
        return super().delete(request, *args, **kwargs)



