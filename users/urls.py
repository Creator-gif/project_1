from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, StudentProfileView, TeacherProfileView

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  # Добавьте эту строку
    path('student_profile/', StudentProfileView.as_view(), name='student-profile'),
    path('teacher_profile/', TeacherProfileView.as_view(), name='teacher-profile'),
]