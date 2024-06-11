from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    photo_profile = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    TYPE_USER_CHOICES = [
        (1, 'Siswa'),
        (2, 'Guru'),
        (3, 'CEO'),
        (4, 'Developer'),
        (5, 'Admin'),
    ]

    KELAS_CHOICES = [
        (1, 'X'),
        (2, 'XI'),
        (3, 'XII'),
    ]

    JURUSAN_CHOICES = [
        (1, 'AKL'),
        (2, 'APHP'),
        (3, 'TBSM'),
        (4, 'TJKT'),
        (5, 'TKRO'),
        (6, 'TP'),
    ]

    typer_user = models.PositiveSmallIntegerField(choices=TYPE_USER_CHOICES, null=True)
    kelas = models.PositiveSmallIntegerField(choices=KELAS_CHOICES, null=True)
    jurusan = models.PositiveSmallIntegerField(choices=JURUSAN_CHOICES, null=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    
    def __str__(self):
     return self.user.first_name

class ProfileSiswa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg', blank=True, null=True)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return self.user.username

class Kategori(models.Model):
    nama = models.CharField(max_length=64)

    def __str__(self):
        return self.nama

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('wow', 'Wow'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    emoji_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reacted {self.reaction_type} to {self.post.title}"

class Buku(models.Model):
    judul = models.CharField(max_length=255)
    sinopsis = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    buku_link = models.CharField(max_length=255, null=True)
    sampul = models.ImageField(upload_to='sampul_buku/')

    def __str__(self):
        return self.judul
class Blog(models.Model):
    judul = models.CharField(max_length=255)
    isi = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tgl_dibuat = models.DateTimeField(auto_now_add=True)
    terakhir_diubah = models.DateTimeField(auto_now=True)
    gambar = models.ImageField(upload_to='blog_banners/')
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_blogs', through='Like')
    
    def __str__(self):
        return self.judul



class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CommentBlog(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isi = models.TextField()
    tgl_dibuat = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.blog.judul}"

class Puisi(models.Model):
    judul = models.CharField(max_length=255)
    isi = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

class CeritaPendek(models.Model):
    judul = models.CharField(max_length=255)
    isi = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

class Berita(models.Model):
    judul = models.CharField(max_length=255)
    isi_berita = models.TextField()
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    banner_berita = models.ImageField(upload_to='berita_banners/')

    def __str__(self):
        return self.judul
