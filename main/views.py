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
from django.http import HttpResponseRedirect


def BuatBlog(request):
 if request.method == 'POST':
  if all(request.POST.get(key) for key in ['judul', 'isi', 'nama_pengguna', 'banner']):
   form = Blog()
   form.judul = request.POST.get('judul')
   form.isi = request.POST.get('isi')
   form.nama_pengguna = request.POST.get('nama_pengguna')
   form.banner = request.POST.get('banner')
   form.save()
   return HttpResponseRedirect("/blog")
 else:
  form = Blog()
 return render(request, 'users/blog.html', {'form': form})






# class BuatBuku(LoginRequiredMixin, CreateView):
#     model = Buku
#     form_class = BukuForm
#     template_name = 'users/buku.html'
#     success_url = '/success'  # Atur ke URL yang sesuai
# 
# 
# 
# class BuatBlog(CreateView):
#     model = Blog
#     form_class = BlogForm
#     template_name = 'users/blog.html'
#     success_url = 'blog'
# 
# 
# 
# 
# class BuatCerita(CreateView):
#     model = CeritaPendek
#     form_class = CerPenForm
#     template_name = 'users/cerpen.html'
#     success_url = '/success/' 
#     
# class BuatBerita(CreateView):
#     model = Berita
#     form_class = BeritaForm
#     template_name = 'users/berita.html'
#     success_url = '/success/' 
# 
def home(request):
 # Get the current user's data

 # Combine the first name and last name into a single string for the "penulis" field
 blogs = Blog.objects.all()
 context = { 'blogs': blogs}
 return render(request, "home/home.html", context)


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
         error_message = "Username atau Password Salah !"
    else:
     error_message = None
    return render(request, 'registration/login.html', {'error_message': error_message})




def dashboard_view(request):
    user = request.user  # Mengambil objek pengguna saat ini
    if user.is_authenticated:
        return render(request, 'users/dashboard.html', {'user': user})
    else:
        return redirect('login')





class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    


def blog(request):
    # Get the current user's data
    user = request.user

    # Combine the first name and last name into a single string for the "penulis" field
    default_penulis = f"{user.first_name} {user.last_name}"

    if request.method == 'POST':
        # Process the form submitted by the user
        form = BlogForm(request.POST)
        if form.is_valid():
            # Create an instance of the Blog model and populate it with form data
            blog = Blog(
                nama_pengguna=form.cleaned_data['nama_pengguna'],
                judul=form.cleaned_data['judul'],
                isi=form.cleaned_data['isi'],
            )
            blog.save()  # Save the instance to the database

            # Redirect to a success page or another appropriate page
            return redirect('/blog')
    else:
        form = BlogForm(initial={'penulis': default_penulis})
    form = BlogForm()
    form.fields['judul'].widget.attrs.update({'class': 'input input-bordered input-primary w-full mt-2 input-custom','placeholder': 'Masukkan Judul...'})
    form.fields['isi'].widget.attrs.update({'class': 'textarea textarea-primary textarea-lg w-full mt-2 textarea-custom', 'placeholder': 'Masukkan Isi...'})
    form.fields['nama_pengguna'].widget.attrs.update({'class': 'textarea textarea-primary textarea-lg w-full mt-2 textarea-custom', 'value': default_penulis})
    blogs = Blog.objects.all()

    context = {'form': form, 'username': user.username, 'blogs': blogs}
    return render(request, 'users/blog.html', context)
