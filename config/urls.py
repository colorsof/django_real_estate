
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


# Admin URL can be configured via DJANGO_ADMIN_URL env var
admin_path = getattr(settings, 'ADMIN_URL', None) or 'admin/'

urlpatterns = [
    # expose admin only at the configured ADMIN_URL (useful for obscuring admin)
    path(settings.ADMIN_URL, admin.site.urls),
    #path(admin_path, admin.site.urls),    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("api/v1/auth/", include("djoser.urls")),        
    path("api/v1/auth/", include("core_apps.users.urls")),  # Custom auth URLs
    #path("api/v1/auth/", include("social_django.urls", namespace="social")),  # Social auth URLs
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/apartment/", include("core_apps.apartments.urls")),  # Apartment app URLs
    path("api/v1/issues/", include("core_apps.issues.urls")),  # Issues app URLs
    path("api/v1/reports/", include("core_apps.reports.urls")),
    path("api/v1/ratings/", include("core_apps.ratings.urls")),
]

admin.site.site_header = "Real Estate Admin"
admin.site.site_title = "Real Estate Admin Portal"
admin.site.index_title = "Welcome to Real Estate Admin Portal"  