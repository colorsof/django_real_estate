import django
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from super_admin.admin.super_admin import super_admin_site
from django.urls import reverse_lazy
from django.views.generic import RedirectView
auth_views = django.contrib.auth.views


def login_view(request):
    return render(request, 'login.html')