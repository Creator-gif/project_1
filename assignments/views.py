from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Assignment
from .forms import AssignmentForm

class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment  # Используем нашу модель
    template_name = 'assignments/list.html'  # Используем этот шаблон

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Assignment.objects.filter(created_by=user)
        elif user.is_student:
            return Assignment.objects.filter(status='published')
        return Assignment.objects.none()

class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/new.html'
    success_url = '/assignments/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_teacher

class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/edit.html'
    success_url = '/assignments/'

    def get_queryset(self):
        return Assignment.objects.filter(created_by=self.request.user)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_teacher