from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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