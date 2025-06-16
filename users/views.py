from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Используем этот шаблон
    redirect_authenticated_user = True  # Если уже вошёл - перенаправит на главную

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # После выхода - на главную