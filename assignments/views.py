from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionGradeForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from users.models import User
from notifications.models import Notification

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
        response = super().form_valid(form)
        students = User.objects.filter(is_student=True)
        for student in students:
            Notification.objects.create(
                user=student,
                message=f"Доступно новое задание: '{form.instance.title}'",
                url=reverse('assignment-detail', kwargs={'pk': form.instance.pk}),
                icon="📝"
            )
        return response

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

class SubmissionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Submission
    fields = ['file']
    template_name = 'assignments/submission_form.html'
    
    def test_func(self):
        # Только студенты могут загружать решения
        return self.request.user.is_student
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment'] = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        
        # Проверка что студент не отправлял решение ранее
        if Submission.objects.filter(assignment=assignment, student=self.request.user).exists():
            form.add_error(None, "Вы уже отправили решение для этого задания")
            return self.form_invalid(form)
        
        form.instance.assignment = assignment
        form.instance.student = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('assignment-detail', kwargs={'pk': self.kwargs['pk']})

class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'assignments/assignment_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        # Для студентов: ищем их отправку (если есть)
        user = self.request.user
        assignment = self.get_object()
        if user.is_student:
            context['user_submission'] = Submission.objects.filter(assignment=assignment, student=user).first()
        else:
            context['user_submission'] = None
        return context
    
class SubmissionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Submission
    template_name = 'assignments/submission_list.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        return Submission.objects.filter(assignment=assignment)

    def test_func(self):
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        return self.request.user == assignment.created_by

class SubmissionGradeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Submission
    form_class = SubmissionGradeForm  # <-- добавьте это!
    template_name = 'assignments/submission_grade.html'

    def get_success_url(self):
        return self.object.assignment.get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().assignment.created_by
    
    def form_valid(self, form):
        response = super().form_valid(form)

        Notification.objects.create(
            user=self.object.student,
            message=f"Ваша работа по заданию '{self.object.assignment.title}' оценена: {self.object.grade}/{self.object.assignment.max_score}",
            url=reverse('assignment-detail', kwargs={'pk': self.object.assignment.pk}),
            icon="🎯"
        )

        return response

