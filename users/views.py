from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm

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