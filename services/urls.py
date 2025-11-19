"""
Services App URLs
"""

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_pro, name='services'),
    path('list/', views.ServiceListView.as_view(), name='services_list'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
]


