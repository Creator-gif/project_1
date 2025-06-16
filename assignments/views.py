from django.views.generic import ListView
from .models import Assignment

class AssignmentListView(ListView):
    model = Assignment  # Используем нашу модель
    template_name = 'assignments/list.html'  # Используем этот шаблон