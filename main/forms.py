from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)  # Nama Lengkap
    last_name = forms.CharField(max_length=100, required=True)  # Nama Lengkap
    profile_picture = forms.ImageField(required=False)  # Bidang Foto Profil

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture']
