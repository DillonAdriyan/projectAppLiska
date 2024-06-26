from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Buku, Blog, CeritaPendek, Berita, Puisi, CustomUser, UserProfile, Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# myapp/forms.py


class GptForm(forms.Form):
    prompt = forms.CharField(label='Enter a prompt', max_length=1000)

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'grow hidden', 'value': '{{ user.username }}'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'grow', 'value': '{{ user.email }}'}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'grow', 'value': '{{ user.first_name }}'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'grow', 'value': '{{ user.last_name }}'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

class UpdateProfileForm(forms.ModelForm):
    photo_profile = forms.ImageField(widget=forms.FileInput(attrs={'class': 'grow hidden'}), required=False)
    typer_user = forms.ChoiceField(choices=UserProfile.TYPE_USER_CHOICES, required=False, widget=forms.Select(attrs={'class': 'grow'}))
    kelas = forms.ChoiceField(choices=UserProfile.KELAS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'grow'}))
    jurusan = forms.ChoiceField(choices=UserProfile.JURUSAN_CHOICES, required=False, widget=forms.Select(attrs={'class': 'grow'}))
    tanggal_lahir = forms.DateField(required=False, widget=forms.SelectDateWidget(
            attrs={'class': 'grow'},
            years=range(1990, 2011)
        ))

    class Meta:
        model = UserProfile
        fields = ['photo_profile', 'typer_user', 'kelas', 'jurusan', 'tanggal_lahir']

    def __init__(self, *args, **kwargs):
        userprofile = kwargs.pop('userprofile', None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        
        if userprofile:
            self.fields['photo_profile'].initial = userprofile.photo_profile
            self.fields['typer_user'].initial = userprofile.typer_user
            self.fields['kelas'].initial = userprofile.kelas
            self.fields['jurusan'].initial = userprofile.jurusan
            self.fields['tanggal_lahir'].initial = userprofile.tanggal_lahir




class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create Post'))

    class Meta:
        model = Post
        fields = ['title', 'content']


class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pw1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pw2'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input input-bordered input-primary w-full'
        self.fields['email'].widget.attrs['class'] = 'input input-bordered input-primary w-full'
        self.fields['password'].widget.attrs['class'] = 'input input-bordered input-primary w-full'
        self.fields['password2'].widget.attrs['class'] = 'input input-bordered input-primary w-full'
        self.fields['first_name'].widget.attrs['class'] = 'input input-bordered input-primary w-full'
        self.fields['last_name'].widget.attrs['class'] = 'input input-bordered input-primary w-full'
        self.fields['typer_user'] = forms.ChoiceField(choices=UserProfile.TYPE_USER_CHOICES, required=False, widget=forms.Select(attrs={'class': 'select select-primary w-full'}))
        self.fields['kelas'] = forms.ChoiceField(choices=UserProfile.KELAS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'select select-primary w-full'}))
        self.fields['jurusan'] = forms.ChoiceField(choices=UserProfile.JURUSAN_CHOICES, required=False, widget=forms.Select(attrs={'class': 'select select-primary w-full'}))
        self.fields['photo_profile'] = forms.ImageField(label='Photo Profile', required=False, widget=forms.FileInput(attrs={'class': 'file-input file-input-bordered input-primary w-full'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Password dan konfirmasi password tidak cocok")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                user_profile.photo_profile = self.cleaned_data['photo_profile']
                user_profile.typer_user = self.cleaned_data['typer_user']
                user_profile.kelas = self.cleaned_data['kelas']
                user_profile.jurusan = self.cleaned_data['jurusan']
                user_profile.save()
        return user


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture']


class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = ['judul', 'sinopsis', 'buku_link', 'created_by', 'sampul']
        widgets = {
            'created_by': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['created_by'].initial = self.user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.created_by_id:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['judul', 'isi', 'gambar', 'kategori', 'created_by']
        widgets = {
            'isi': forms.Textarea(attrs={'class': 'markdown-editor'}),
            'created_by': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['created_by'].initial = self.user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.created_by_id:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class PuisiForm(forms.ModelForm):
    class Meta:
        model = Puisi
        fields = ['judul', 'isi', 'created_by']
        widgets = {
            'created_by': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['created_by'].initial = self.user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.created_by_id:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class CeritaForm(forms.ModelForm):
    class Meta:
        model = CeritaPendek
        fields = ['judul', 'isi', 'created_by']
        widgets = {
            'created_by': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['created_by'].initial = self.user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.created_by_id:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'isi_berita', 'banner_berita', 'kategori', 'created_by']
        widgets = {
            'created_by': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['created_by'].initial = self.user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.created_by_id:
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance
