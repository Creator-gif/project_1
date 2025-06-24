from django.urls import path
from .views import (
    AssignmentListView,
    AssignmentCreateView,
    AssignmentUpdateView,
    AssignmentDetailView,
    SubmissionCreateView,
    SubmissionListView,
    SubmissionGradeView,
)

urlpatterns = [
    path('', AssignmentListView.as_view(), name='assignment-list'),
    path('new/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('<int:pk>/edit/', AssignmentUpdateView.as_view(), name='assignment-edit'),
    path('<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('submit/<int:pk>/', SubmissionCreateView.as_view(), name='submission-create'),
    path('<int:pk>/submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('submission/<int:pk>/grade/', SubmissionGradeView.as_view(), name='submission-grade'),
]