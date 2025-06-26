from django.db import models
from users.models import User
from django.urls import reverse

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255, verbose_name="Текст уведомления")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    url = models.CharField(max_length=200, blank=True, verbose_name="Ссылка для перехода")
    icon = models.CharField(max_length=50, default="📢", verbose_name="Иконка")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}..."

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def get_absolute_url(self):
        return self.url if self.url else reverse('notifications-list')