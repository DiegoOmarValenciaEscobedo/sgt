from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        label="Correo electrónico",
        widget=forms.TextInput(attrs={'id': 'email'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'id': 'password',})
    )