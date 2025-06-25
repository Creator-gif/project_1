from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.db.models import Avg, Count
from assignments.models import Submission, Assignment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Используем этот шаблон
    redirect_authenticated_user = True  # Если уже вошёл - перенаправит на главную

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # После выхода - на главную

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_approved:
                return render(request, 'users/login.html', {'error': 'Ваш аккаунт ещё не подтверждён администратором.'})
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Неверные данные'})
    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/register_done.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

class StudentProfileView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/student_profile.html'
    
    def test_func(self):
        return self.request.user.is_student
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user
        
        # Статистика
        submissions = Submission.objects.filter(student=student).select_related('assignment')
        completed = submissions.count()
        avg_grade = submissions.aggregate(avg=Avg('grade'))['avg'] or 0
        
        context.update({
            'submissions': submissions,
            'completed_assignments': completed,
            'avg_grade': round(avg_grade, 1),
            'late_submissions': submissions.filter(is_late=True).count()
        })
        return context
    
class TeacherProfileView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/teacher_profile.html'
    
    def test_func(self):
        return self.request.user.is_teacher
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user
        
        assignments = Assignment.objects.filter(created_by=teacher)
        submissions = Submission.objects.filter(assignment__in=assignments)
        
        context.update({
            'assignments': assignments,
            'ungraded_submissions': submissions.filter(grade__isnull=True).count(),
            'active_assignments': assignments.filter(status='published').count(),
            'top_students': submissions.values('student').annotate(
                avg_grade=Avg('grade')
            ).order_by('-avg_grade')[:5]
        })
        return context