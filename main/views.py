from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm, BukuForm, BlogForm, CerPenForm, BeritaForm
# views.py
from django.views.generic.edit import CreateView
from .models import Buku, Blog, CeritaPendek, Berita
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import View

class BuatBuku(CreateView):
    model = Buku
    form_class = BukuForm
    template_name = 'users/buku.html'
    success_url = '/success'  # Atur ke URL yang sesuai

class BuatBlog(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'users/blog.html'
    success_url = 'blog'

    def form_valid(self, form):
        form.instance.penulis = self.request.user.first_name + " " + self.request.user.last_name
        return super().form_valid(form)




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


class DashboardBase(LoginRequiredMixin, View):
    template_name = "users/dashboard.html"  # Template dasar untuk dasbor

    def get(self, request):
        username = request.user.username  # Mengambil username dari pengguna saat ini
        context = {'username': username}
        return render(request, self.template_name, context)



class BukuDashboard(DashboardBase):
    template_name = "users/buku.html"  # Template khusus untuk halaman buku

class BeritaDashboard(DashboardBase):
    template_name = "users/berita.html"  # Template khusus untuk halaman berita

class BlogDashboard(DashboardBase):
    template_name = "users/blog.html"  # Template khusus untuk halaman blog

class CerpenDashboard(DashboardBase):
    template_name = "users/cerpen.html"  # Template khusus untuk halaman CerpenDashboard



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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            return redirect('dashboard')
        else:
            return "Username atau Password salah"
    return render(request, 'registration/login.html')




def dashboard_view(request):
    user = request.user  # Mengambil objek pengguna saat ini
    if user.is_authenticated:
        return render(request, 'users/dashboard.html', {'user': user})
    else:
        return redirect('login')





class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    



# buku def
@login_required
def buku(request):
    # Dapatkan data pengguna saat ini
    user = request.user

    # Gabungkan nama depan dan nama belakang menjadi satu string untuk field "penulis"
    default_penulis = f"{user.first_name} {user.last_name}"

    # Buat form dan atur nilai default untuk field "penulis"
    form = BukuForm(initial={'penulis': default_penulis})

    if request.method == 'POST':
        # Proses form yang dikirim oleh pengguna
        form = BukuForm(request.POST, request.FILES)

        if form.is_valid():
            # Simpan data buku ke dalam database
            buku = form.save()
            # Redirect ke halaman sukses atau halaman lain yang sesuai
            return redirect('success')

    return render(request, 'users/buku.html', {'form': form})
    


# blog def
@login_required
def blog(request):
    # Dapatkan data pengguna saat ini
    user = request.user

    # Gabungkan nama depan dan nama belakang menjadi satu string untuk field "penulis"
    default_penulis = f"{user.first_name} {user.last_name}"

    # Buat form dan atur nilai default untuk field "penulis"
    form = BlogForm(initial={'penulis': default_penulis})

    if request.method == 'POST':
        # Proses form yang dikirim oleh pengguna
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            # Simpan data buku ke dalam database
            Blog = form.save()
            # Redirect ke halaman sukses atau halaman lain yang sesuai
            return redirect('success')
    context = {'form': form, 'username': user.username}
    return render(request, 'users/blog.html', {'form': form})


# berita def
@login_required
def berita(request):
    # Dapatkan data pengguna saat ini
    user = request.user

    # Gabungkan nama depan dan nama belakang menjadi satu string untuk field "penulis"
    default_penulis = f"{user.first_name} {user.last_name}"

    # Buat form dan atur nilai default untuk field "penulis"
    form = BeritaForm(initial={'penulis': default_penulis})

    if request.method == 'POST':
        # Proses form yang dikirim oleh pengguna
        form = BeritaForm(request.POST, request.FILES)

        if form.is_valid():
            # Simpan data buku ke dalam database
            berita = form.save()
            # Redirect ke halaman sukses atau halaman lain yang sesuai
            return redirect('success')

    return render(request, 'users/berita.html', {'form': form})

# cerita def
@login_required
def cerita(request):
    # Dapatkan data pengguna saat ini
    user = request.user

    # Gabungkan nama depan dan nama belakang menjadi satu string untuk field "penulis"
    default_penulis = f"{user.first_name} {user.last_name}"

    # Buat form dan atur nilai default untuk field "penulis"
    form = CerPenForm(initial={'penulis': default_penulis})

    if request.method == 'POST':
        # Proses form yang dikirim oleh pengguna
        form = CerPenForm(request.POST, request.FILES)

        if form.is_valid():
            # Simpan data buku ke dalam database
            cerita = form.save()
            # Redirect ke halaman sukses atau halaman lain yang sesuai
            return redirect('success')

    return render(request, 'users/cerpen.html', {'form': form})
