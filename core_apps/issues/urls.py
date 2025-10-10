from django.urls import path, include

from .views import IssueListAPIView, IssueCreateAPIView, IssueDeleteAPIView, \
    IssueUpdateAPIView, IssueDetailAPIView,MyIssuesListView, AssignedIssuesListView

urlpatterns = [
    path('', IssueListAPIView.as_view(), name='issue-list'),
    path("me/", MyIssuesListView.as_view(), name="my-issues"),
    path("assigned/", AssignedIssuesListView.as_view(), name="assigned-issues"),
    path('create/<uuid:apartment_id>/', IssueCreateAPIView.as_view(), name='create-issue'),
    path('update/<uuid:id>/', IssueUpdateAPIView.as_view(), name='update-issue'),
    path('delete/<uuid:id>/', IssueDeleteAPIView.as_view(), name='delete-issue'),
    path('<uuid:id>/', IssueDetailAPIView.as_view(), name='issue-detail'),
]