from django import forms
from .models import User

class LoginForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username', 'password',)
