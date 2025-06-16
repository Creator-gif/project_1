from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Добавляем кастомные поля в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_teacher', 'is_student')}),
    )
    # Добавляем кастомные поля в список пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_teacher', 'is_student')


    # Фильтры для списка пользователей
    list_filter = ('is_teacher', 'is_student')
    
    # Поиск по полям
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Группировка полей в форме создания
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('is_teacher', 'is_student'),
        }),
    )
# Регистрируем кастомную модель
admin.site.register(User, CustomUserAdmin)