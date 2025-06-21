from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

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
            login(request, user)
            return redirect('templates/home.html')  # или другой маршрут
        else:
            return render(request, 'users/login.html', {'error': 'Неверные данные'})
    return render(request, 'users/login.html')