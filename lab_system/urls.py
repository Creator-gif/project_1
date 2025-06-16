"""
URL configuration for lab_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # Для простых страниц
from users.views import CustomLoginView
from users.views import CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),          # Админка
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  # Главная страница
    path('assignments/', include('assignments.urls')),  # Все пути для заданий
    path('login/', CustomLoginView.as_view(), name='login'), # Добавьте этот путь для входа:
    path('logout/', CustomLogoutView.as_view(), name='logout'), 
    path('users/', include('users.urls')),    # Все пути для пользователей
]
