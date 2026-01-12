"""
URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.admin_view),
    
    # API endpoints
    path('api/document/', include('django_app.apps.document_processor.urls')),
    path('api/validation/', include('django_app.apps.estimation_validator.urls')),
    
    # Health check
    path('health/', lambda request: __import__('django.http').HttpResponse('OK')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
