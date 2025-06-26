from notifications.models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        unread_notes = Notification.objects.filter(user=request.user, is_read=False)
        all_notes = Notification.objects.filter(user=request.user)
    else:
        unread_notes = []
        all_notes = []
    return {
        'unread_notes': unread_notes,
        'all_notes': all_notes,
    }