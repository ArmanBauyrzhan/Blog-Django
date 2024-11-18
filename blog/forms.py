from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'cols': 60, 'rows': 10}),
            'email': forms.EmailInput(attrs={'cols': 60, 'rows': 10}),
            'password1': forms.PasswordInput(attrs={'cols': 60, 'rows': 10}),
            'password2': forms.PasswordInput(attrs={'cols': 60, 'rows': 10}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'content', 'is_public', 'is_visible_on_request', 'tags')

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),  # Передаем Manager для корректного выбора тегов
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # С какой моделью работаем
        fields = ('content',) # Какие поля будут доступны в форме
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите ваш комментарий...',
                'rows': 3,
            }),
        }