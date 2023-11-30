from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission, AbstractUser

# class CustomUser(AbstractUser):
#     groups = models.ManyToManyField(Group, through='GroupSiswa', related_name='custom_users_groups')
#     user_permissions = models.ManyToManyField(Permission, through='PermissionSiswa', related_name='custom_users_permissions')
# 
# 
# class Siswa(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
#     jabatan = models.CharField(max_length=20)
# 
# 
#     def __str__(self):
#      return f"{self.first_name} {self.last_name}"
# 
# Membuat model perantara untuk relasi many-to-many
# class GroupSiswa(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_siswa_set')
#     customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='group_set')
# 
# class PermissionSiswa(models.Model):
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='permission_siswa_set')
#     customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='permission_set')



# Mengatasi konflik
# Group.add_to_class('siswa_set', models.ManyToManyField(CustomUser, through='GroupSiswa'))
# Permission.add_to_class('siswa_set', models.ManyToManyField(CustomUser, through='PermissionSiswa'))

#     def __str__(self):
#         return self.user.username
    # Tambahkan bidang-bidang kustom lainnya sesuai kebutuhan (misalnya, tanggal lahir, dll.)



# Create your models here.

class CustomUser(AbstractUser):
    # Tambahkan metode atau bidang khusus di sini jika dibutuhkanfirst
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, related_name='custom_user_group')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permission'
    )

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    photo_profile = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    TYPER_USER_CHOICES = (
        (1, 'Siswa'),
        (2, 'Guru'),
        (3, 'CEO'),
        (4, 'Developer'),
        (5, 'admin'),
    )

    KELAS_CHOICES = (
        (1, 'X'),
        (2, 'XI'),
        (3, 'XII'),
    )

    JURUSAN_CHOICES = (
        (1, 'AKL'),
        (2, 'APHP'),
        (3, 'TBSM'),
        (4, 'TJKT'),
        (5, 'TKRO'),
        (6, 'TP'),
    )

    # Definisikan field lainnya di sini

    typer_user = models.PositiveSmallIntegerField(choices=TYPER_USER_CHOICES, null=True)
    kelas = models.PositiveSmallIntegerField(choices=KELAS_CHOICES, null=True)
    jurusan = models.PositiveSmallIntegerField(choices=JURUSAN_CHOICES, null=True)
    tanggal_lahir = models.DateField(null=True, blank=True)


class ProfileSiswa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg', blank=True, null=True)
    
    class Meta:
     ordering = ["first_name", "last_name", "profile_picture"]
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

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class Reaction(models.Model):
    REACTION_CHOICES = (
        ('like', 'Like'),
        ('love', 'Love'),
        ('wow', 'Wow'),
        # Tambahkan reaksi lainnya sesuai kebutuhan
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    emoji_url = models.URLField(blank=True)  # Menyimpan URL emoji/gambar
    created_at = models.DateTimeField(auto_now_add=True)
    



class Buku(models.Model):
    judul = models.CharField(max_length=255)
    sinopsis = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    buku_pdf = models.FileField(upload_to='buku_pdfs/')
    sampul = models.ImageField(upload_to='sampul_buku/')
    def __str__(self):
     return self.judul

class Blog(models.Model):
    judul = models.CharField(max_length=255)
    isi = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # hubungan dengan Field user custom saya
    tgl_dibuat = models.DateTimeField(auto_now_add=True)
    terakhir_diubah = models.DateTimeField(auto_now=True)
    gambar = models.ImageField(upload_to='blog_banners/')
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    def __str__(self):
     return self.judul
class Comment_Blog(models.Model):
 created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 isi = models.TextField()
 tgl_dibuat = models.DateTimeField(auto_now_add=True)
 blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


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