"""
Services App URLs
"""

from django.urls import path
from . import views


urlpatterns = [
    # Services List
    path('', views.services_pro, name='services'),
    path('list/', views.ServiceListView.as_view(), name='services_list'),

    # Services CRUD (create/edit/delete MUST come before detail with slug)
    path('service/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('service/<slug:slug>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('service/<slug:slug>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    # Service Detail (MUST be last to avoid matching 'create', 'edit', 'delete' as slugs)
    path('service/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
]


