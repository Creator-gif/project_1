from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import redirect
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.notifications.all()

class MarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = request.user.notifications.get(pk=pk)
        notification.mark_as_read()
        return redirect(notification.get_absolute_url())

class MarkAllAsReadView(LoginRequiredMixin, View):
    def post(self, request):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return redirect('notifications-list')