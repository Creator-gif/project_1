from django.urls import path
from .views import NotificationListView, MarkAsReadView, MarkAllAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/read/', MarkAsReadView.as_view(), name='notification-read'),
    path('read-all/', MarkAllAsReadView.as_view(), name='notifications-mark-all-read'),
]