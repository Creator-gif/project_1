from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_teacher', 'is_student', 'is_approved')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_teacher', 'is_student', 'is_approved')
    list_filter = ('is_teacher', 'is_student', 'is_approved')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('is_teacher', 'is_student', 'is_approved'),
        }),
    )

admin.site.register(User, CustomUserAdmin)