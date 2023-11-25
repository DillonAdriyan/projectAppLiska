from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Buku, Blog, CeritaPendek, Berita, Puisi, CustomUser, UserProfile



class CustomRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))  # Tambahkan field konfirmasi password

    class Meta:
        model = CustomUser
        fields = ('username', 'email','password', 'first_name', 'last_name')  # Hapus 'password', tambahkan 'password2' di sini

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Menambahkan kelas CSS ke dalam widget untuk setiap field
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'

        # Menggunakan ChoiceField untuk field yang ingin ditampilkan sebagai pilihan
        self.fields['typer_user'] = forms.ChoiceField(choices=UserProfile.TYPER_USER_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['kelas'] = forms.ChoiceField(choices=UserProfile.KELAS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['jurusan'] = forms.ChoiceField(choices=UserProfile.JURUSAN_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['photo_profile'] = forms.ClearableFileInput(attrs={'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Password dan konfirmasi password tidak cocok")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'password' in self.changed_data:  # Cek apakah password telah diubah
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            user_profile = UserProfile.objects.get_or_create(user=user)[0]
            user_profile.typer_user = self.cleaned_data.get('typer_user')
            user_profile.kelas = self.cleaned_data.get('kelas')
            user_profile.jurusan = self.cleaned_data.get('jurusan')
            user_profile.photo_profile = self.cleaned_data.get('photo_profile')
            user_profile.save()
        return user


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
        fields = ['judul', 'isi', 'user', 'gambar', 'kategori']
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
        fields = ['judul', 'isi', 'pengguna' ]
# form blog
class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'isi_berita', 'jenis_berita',   'ditulis_oleh', 'banner_berita']

