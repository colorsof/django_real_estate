from django.urls import path
from .views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProfileUpdateAPIView,
    AvatarUploadAPIView,
    NonTenantProfileListAPIView
)
urlpatterns = [
    path('all/', ProfileListAPIView.as_view(), name='profile-list'),
    path('non-tenant-profiles/', NonTenantProfileListAPIView.as_view(),
         name='non-tenant-profiles'),
    path('user/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('user/my-profile/', ProfileDetailAPIView.as_view(), name='profile-detail'),    
    path('user/avatar/', AvatarUploadAPIView.as_view(), name='avatar-upload'),
]