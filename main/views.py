from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm, BukuForm, BlogForm, CerPenForm, BeritaForm
# views.py
from django.views.generic.edit import CreateView
from .models import Buku, Blog, CeritaPendek, Berita

class BuatBuku(CreateView):
    model = Buku
    form_class = BukuForm
    template_name = 'users/buku.html'
    success_url = '/success'  # Atur ke URL yang sesuai

class BuatBlog(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'users/blog.html'
    success_url = '/success/'  # Atur ke URL yang sesuai
    
class BuatCerita(CreateView):
    model = CeritaPendek
    form_class = CerPenForm
    template_name = 'users/cerpen.html'
    success_url = '/success/' 
    
class BuatBerita(CreateView):
    model = Berita
    form_class = BeritaForm
    template_name = 'users/berita.html'
    success_url = '/success/' 

def home(request):
 return render(request, "home/home.html")

def dashboard(request):
    return render(request, "users/dashboard.html")
def buku(request):
    return render(request, "users/buku.html")
def berita(request):
    return render(request, "users/berita.html")
def blog(request):
    return render(request, "users/blog.html")
def cerpen(request):
    return render(request, "users/cerpen.html")

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Simpan objek User dari formulir
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    # Proses login, verifikasi pengguna, dan set sesi jika login berhasil
    if login_berhasil:
        request.session['user_id'] = user.id  # Menyimpan ID pengguna dalam sesi
        return redirect('dashboard')  # Ganti 'dashboard' dengan nama rute halaman dasbor
    else:
     return "Username atau Password salah"

def dashboard_view(request):
    user_id = request.session.get('user_id')  # Mengambil ID pengguna dari sesi
    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        return "Tidak ada ID pengguna dalam sesi, pengguna belum masuk"
        

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    