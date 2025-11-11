from django.shortcuts import get_object_or_404,render
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.views.generic import TemplateView


def admin_profile(request):
    return render(request, 'tenants/admin_profile.html')

