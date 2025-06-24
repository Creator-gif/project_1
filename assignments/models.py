from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import User

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    max_score = models.IntegerField(default=100, verbose_name="Максимальный балл")  # Добавьте это поле

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('assignment-detail', args=[str(self.pk)])

def submission_file_path(instance, filename):
    return f'submissions/assignment_{instance.assignment.id}/user_{instance.student.id}/{filename}'

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to=submission_file_path)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(null=True, blank=True, verbose_name="Оценка")
    feedback = models.TextField(blank=True, verbose_name="Комментарий")
    is_late = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Автоматическая проверка сдачи после дедлайна
        if self.assignment.due_date < timezone.now():
            self.is_late = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"