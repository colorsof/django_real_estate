import logging
from typing import Any

from django.http import Http404
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response


from .models import Issue
from .serializers import IssueSerializer, IssueStatusUpdateSerializer
from .emails import send_issue_confirmation_email, send_issue_resolved_email
from core_apps.apartments.models import Apartment
from core_apps.common.models import ContentView
from core_apps.common.renderers import GenericJSONRenderer


logger = logging.getLogger(__name__)


class IsStaffOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow staff or superusers to access certain views.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        is_authorized = (request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser))
        if not is_authorized:
            self.message = ("Access to this resource is restricted to staff or admin users only.")
        return is_authorized

class IssueListAPIView(generics.ListAPIView):
    """
    API view to list all issues. Accessible only by staff or superusers.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsStaffOrSuperUser]
    renderer_classes = [GenericJSONRenderer]
    object_label = "issues"
    
class AssignedIssuesListView(generics.ListAPIView):
    
    #queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    #permission_classes = [IsStaffOrSuperUser]
    renderer_classes = [GenericJSONRenderer]
    object_label = "assigned_issues"    
    
    def get_queryset(self):
        user = self.request.user         
        return Issue.objects.filter(assigned_to=user)  #super().get_queryset().filter(assigned_to=user)


class MyIssuesListView(generics.ListAPIView):

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    #permission_classes = [IsStaffOrSuperUser]
    renderer_classes = [GenericJSONRenderer]
    object_label = "my_issues"
    
    def get_queryset(self):
        user = self.request.user         
        return Issue.objects.filter(reported_by=user)
    
class IssueCreateAPIView(generics.CreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer    
    renderer_classes = [GenericJSONRenderer]
    object_label = "issues"
    
    def perform_create(self, serializer: IssueSerializer) -> None:
        apartment_id = self.kwargs.get('apartment_id')
        
        if not apartment_id:
            raise ValidationError({"Apartment ID":["Apartment ID is required to report an issue."]})
        
        try:
            apartment = Apartment.objects.get(id=apartment_id, tenant=self.request.user)
            
        except Apartment.DoesNotExist:
            raise PermissionDenied("You do not have permission to report an issue for this apartment.")
        issue = serializer.save(reported_by=self.request.user, apartment=apartment)        
        send_issue_confirmation_email(issue)


class IssueDetailAPIView(generics.RetrieveAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_field = "id"
    renderer_classes = [GenericJSONRenderer]
    object_label = "issue"
    
    def get_object(self) -> Issue:
        issue = super().get_object()
        user = self.request.user
        if not (
            user == issue.reported_by or user.is_staff or user == issue.assigned_to
        ):
            raise PermissionDenied("You do not have permission to view this issue.")
        self.record_issue_view(issue)
        return issue
    
    def  record_issue_view(self, issue):
        viewer_ip = self.get_client_ip()
        user = self.request.user
        ContentView.record_view(issue, user, viewer_ip)
        
    def get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        # x_forwarded_for is used when the request has passed through a proxy
        # thus retrieve the first IP in the list as the client's IP thus the commma to split
        # and the [0] to get the first IP
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
class IssueUpdateAPIView(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueStatusUpdateSerializer
    lookup_field = "id"
    renderer_classes = [GenericJSONRenderer]
    object_label = "issue"
    
    def get_object(self) -> Issue:
        issue = super().get_object()
        user = self.request.user
        if not (user.is_staff or user == issue.assigned_to):
            logger.warning(
                f"Unauthorized update attempt by user {user.get_full_name} on issue {issue.title}"
            )
            raise PermissionDenied("You do not have permission to update this issue.")
        send_issue_resolved_email(issue)
        return issue
                       
class IssueDeleteAPIView(generics.DestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_field = "id"
    
    
    def get_object(self) -> Issue:
        try: 
            issue = super().get_object()
        except Http404:
            raise Http404("Issue not found.")
        user = self.request.user
        if not (user.is_staff or  user == issue.reported_by):
            logger.warning(
                f"Unauthorized delete attempt by user {user.get_full_name} on issue {issue.title}"
            )
            raise PermissionDenied("You do not have permission to delete this issue.")
        return issue
    
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        super().delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)