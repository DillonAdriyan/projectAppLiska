from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import RegistrationForm, BukuForm, BlogForm, CeritaForm, BeritaForm, PuisiForm, CustomRegistrationForm, PostForm
# views.py
from django.views.generic.edit import CreateView
from .models import Buku, Blog, CeritaPendek, Berita, Puisi, UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseRedirect
import markdown
import markdown2
from django.contrib.auth import logout
from django.contrib import messages




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
 bukus = Buku.objects.all()
 blogs = Blog.objects.all()
 context = { 'blogs': blogs, 'bukus': bukus}
 return render(request, "home/home.html", context)

def base_nav(request):
 user = request.user
 
class DashboardBase(LoginRequiredMixin, View):
    template_name = "users/dashboard.html"  # Template dasar untuk dasbor

    def get(self, request):
        username = request.user.username  # Mengambil username dari pengguna saat ini
        context = {'username': username}
        return render(request, self.template_name, context)


def register_user(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Periksa apakah UserProfile sudah ada
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                user_profile.photo_profile = form.cleaned_data['photo_profile']
                user_profile.typer_user = form.cleaned_data['typer_user']
                user_profile.kelas = form.cleaned_data['kelas']
                user_profile.jurusan = form.cleaned_data['jurusan']
                user_profile.save()

            login(request, user)
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomRegistrationForm()
    return render(request, 'registration/regist_user.html', {'form': form})



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
            messages.success(request, 'Login berhasil! Selamat datang.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username atau Password Salah !')
            return render(request, 'registration/login.html')
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'registration/login.html')





# logout 

def logout_view(request):
    # Lakukan logout
    logout(request)
    messages.success(request,'Berhasil Logout')
    return redirect('login')



def dashboard_view(request):
    user = request.user  # Mengambil objek pengguna saat ini
    if user.is_authenticated:
        messages.success(request, 'Selamat datang di dashboard, ' + user.username + '!')
        return render(request, 'users/dashboard.html', {'user': user})
    else:
        return redirect('login')






class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            # Sesuaikan penambahan informasi terkait postingan (contoh: author) sebelum disimpan
            new_post.author = request.user  # Atur penulis postingan sesuai pengguna yang sedang login
            new_post.save()
            return redirect('dashboard')  # Ganti 'nama_url' dengan nama URL yang ingin Anda tuju setelah membuat postingan
    else:
        form = PostForm()
    
    return render(request, 'users/create_post.html', {'form': form})
    
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    reaction_choices = Reaction.REACTION_CHOICES  # Mendapatkan pilihan reaksi dari model
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Atur penulis komentar sesuai pengguna yang sedang login
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'detail/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'reaction_choices': reaction_choices,
    })

from django.http import JsonResponse

def add_reaction(request, post_id):
    if request.method == 'POST' and request.is_ajax():
        post = get_object_or_404(Post, id=post_id)
        reaction_type = request.POST.get('reaction')  # Mendapatkan reaksi yang dipilih oleh pengguna

        # Pastikan pengguna sudah login sebelum memberikan reaksi
        if request.user.is_authenticated:
            # Cek apakah pengguna sudah memberikan reaksi sebelumnya pada postingan ini
            existing_reaction = Reaction.objects.filter(post=post, user=request.user).first()
            
            if existing_reaction:
                # Jika sudah memberikan reaksi, perbarui reaksi pengguna
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
            else:
                # Jika belum memberikan reaksi, buat reaksi baru
                Reaction.objects.create(post=post, user=request.user, reaction_type=reaction_type)
            
            # Kirim respons JSON bahwa reaksi berhasil ditambahkan
            return JsonResponse({'success': True, 'message': 'Reaction added successfully'})
        else:
            # Jika pengguna belum login, kirim respons JSON untuk meminta pengguna login
            return JsonResponse({'success': False, 'message': 'Please login to add reaction'})
    
    # Jika bukan metode POST atau bukan permintaan Ajax, kirim respons JSON dengan error
    return JsonResponse({'success': False, 'message': 'Invalid request'})
    


## views blog
@login_required
def blog(request):
    user = request.user
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            return redirect('blog')
        else:
         for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BlogForm(user=user)

    form.fields['judul'].widget.attrs.update({'class': 'input input-bordered input-primary w-full mt-2 input-custom','placeholder': 'Masukkan Judul...'})
    form.fields['isi'].widget.attrs.update({'class': 'textarea textarea-primary textarea-lg w-full mt-2 textarea-custom', 'placeholder': 'Masukkan Isi...'})
    form.fields['gambar'].widget.attrs.update({'class': 'file-input file-input-bordered file-input-primary w-full mt-2'})
    form.fields['kategori'].widget.attrs.update({'class': 'input input-bordered input-primary w-full mt-2'})

    blogs = Blog.objects.filter(created_by=user)
    
    context = {'form': form, 'username': user.username, 'blogs': blogs}
    return render(request, 'users/blog.html', context)



## views puisi
@login_required
def puisi(request):
    user = request.user
    if request.method == 'POST':
        form = PuisiForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('puisi')
        else:
         for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PuisiForm(user=user)

    form.fields['judul'].widget.attrs.update({'class': 'input input-bordered input-primary w-full mt-2 input-custom','placeholder': 'Masukkan Judul...'})
    form.fields['isi'].widget.attrs.update({'class': 'textarea textarea-primary textarea-lg w-full mt-2 textarea-custom', 'placeholder': 'Masukkan Isi...'})

    puisis = Puisi.objects.filter(created_by=user)
    
    context = {'form': form, 'username': user.username, 'puisis': puisis}
    return render(request, 'users/puisi.html', context)

## views buku 
@login_required
def buku(request):
    user = request.user
    if request.method == 'POST':
        form = BukuForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Buku berhasil di upload!")
            return redirect('buku')
        else:
         for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BukuForm(user=user)

    form.fields['judul'].widget.attrs.update({'class': 'input input-bordered input-primary w-full mt-2 input-custom','placeholder': 'Masukkan Judul...'})
    form.fields['sinopsis'].widget.attrs.update({'class': 'textarea textarea-primary textarea-lg w-full mt-2 textarea-custom', 'placeholder': 'Masukkan Isi...'})
    form.fields['buku_pdf'].widget.attrs.update({'class': 'file-input file-input-bordered file-input-primary w-full mt-2'})
    form.fields['sampul'].widget.attrs.update({'class': 'file-input file-input-bordered file-input-primary w-full mt-2'})

    bukus = Buku.objects.filter(created_by=user)
    
    context = {'form': form, 'username': user.username, 'bukus': bukus}
    return render(request, 'users/buku.html', context)

def download_buku(request, buku_id):
    buku = get_object_or_404(Buku, pk=buku_id)
    file_path = buku.file_buku.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

## views berita
@login_required
def berita(request):
    user = request.user
    if request.method == 'POST':
        form = beritaForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            return redirect('berita')
        else:
         for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BeritaForm(user=user)

    form.fields['judul'].widget.attrs.update({'class': 'input input-bordered input-primary w-full mt-2 input-custom','placeholder': 'Masukkan Judul...'})
    form.fields['isi_berita'].widget.attrs.update({'class': 'textarea textarea-primary textarea-lg w-full mt-2 textarea-custom', 'placeholder': 'Masukkan Isi...'})
    form.fields['banner_berita'].widget.attrs.update({'class': 'file-input file-input-bordered file-input-primary w-full mt-2'})
    form.fields['kategori'].widget.attrs.update({'class': 'input input-bordered input-primary w-full mt-2'})

    beritas = Berita.objects.filter(created_by=user)
    
    context = {'form': form, 'username': user.username, 'beritas': beritas}
    return render(request, 'users/berita.html', context)

## views cerita
@login_required
def cerita(request):
    user = request.user
    if request.method == 'POST':
        form = ceritaForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            return redirect('cerita')
        else:
         for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CeritaForm(user=user)

    form.fields['judul'].widget.attrs.update({'class': 'input input-bordered input-primary w-full mt-2 input-custom','placeholder': 'Masukkan Judul...'})
    form.fields['isi'].widget.attrs.update({'class': 'textarea textarea-primary textarea-lg w-full mt-2 textarea-custom', 'placeholder': 'Masukkan Isi...'})

    ceritas = CeritaPendek.objects.filter(created_by=user)
    
    context = {'form': form, 'username': user.username, 'ceritas': ceritas}
    return render(request, 'users/cerpen.html', context)



## fungsi detail
@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.isi = markdown.markdown(blog.isi)
    return render(request, 'detail/blog-detail.html', {'blog': blog})
    
@login_required
def puisi_detail(request, puisi_id):
    puisi = get_object_or_404(Puisi, pk=puisi_id)
    puisi.isi = markdown.markdown(puisi.isi)
    return render(request, 'detail/puisi-detail.html', {'puisi': puisi})
    