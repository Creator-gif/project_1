from django.urls import path
from .views import AssignmentListView, AssignmentCreateView, AssignmentUpdateView

urlpatterns = [
    path('', AssignmentListView.as_view(), name='assignment-list'),
    path('new/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('<int:pk>/edit/', AssignmentUpdateView.as_view(), name='assignment-edit'),
]