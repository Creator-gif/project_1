from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.urls import reverse

from assignments.models import Submission
from notifications.models import Notification

User = get_user_model()


@receiver(post_save, sender=Submission)
def notify_on_submission(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.assignment.created_by,
            message=f"Студент {instance.student.username} отправил решение по заданию '{instance.assignment.title}'",
            url=reverse('submission-grade', kwargs={'pk': instance.pk}),
            icon="📤"
        )


@receiver(post_save, sender=User)
def notify_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_approved:
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"Новый пользователь ожидает подтверждения: {instance.username}",
                url=reverse('admin:users_user_change', args=[instance.id]),
                icon="👤"
            )