from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Электронная почта", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_student', 'is_teacher', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['is_student'].label = 'Студент'
        self.fields['is_teacher'].label = 'Преподаватель'
        # Остальные поля уже с русскими подписями
        for name, field in self.fields.items():
            if name not in ['is_student', 'is_teacher']:
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error('password2', "Пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_approved = False  # Всегда False при регистрации
        if commit:
            user.save()
        return user
