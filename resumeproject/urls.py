"""
URL configuration for resumeproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core import views as core_views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Core pages
    path('', core_views.home_page, name="home"),
    path('about/', core_views.about_page, name="about"),
    path('projects/', core_views.ProjectListView.as_view(), name="projects"),
    path('project/<slug:slug>/', core_views.ProjectDetailView.as_view(), name="project_detail"),

    # App URLs
    path('services/', include('services.urls')),
    path('skills/', include('education.urls')),
    path('contact/', include('contact.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# Custom error handlers
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'


