from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Buku, Blog, CeritaPendek, Berita, Puisi

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)  # Nama Lengkap
    last_name = forms.CharField(max_length=100, required=True)  # Nama Lengkap
    profile_picture = forms.ImageField(required=False)  # Bidang Foto Profil

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture']

# form BukuForm
class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = ['judul', 'sinopsis', 'penulis', 'buku_pdf']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['judul', 'isi', 'nama_pengguna']
        widgets = {
            'isi': forms.Textarea(attrs={'class': 'markdown-editor'}),
        }
        
# puisi form
class PuisiForm(forms.ModelForm):
    class Meta:
        model = Puisi
        fields = ['judul', 'isi', 'penulis']
        widgets = {
            'isi': forms.Textarea(attrs={'class': 'markdown-editor'}),
        }


 
# form blog
class CerPenForm(forms.ModelForm):
    class Meta:
        model = CeritaPendek
        fields = ['judul', 'isi_cerita', 'pengguna' ]
# form blog
class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'isi_berita', 'jenis_berita',   'ditulis_oleh', 'banner_berita']

