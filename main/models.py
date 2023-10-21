from django.db import models
from django.contrib.auth.models import User

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




class ProfileSiswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg', blank=True, null=True)
    
    class Meta:
     ordering = ["first_name", "last_name", "profile_picture"]
    def __str__(self):
        return self.user.username
        

class Berita(models.Model):
    id = models.AutoField(primary_key=True)
    judul = models.CharField(max_length=255)
    isi_berita = models.TextField()
    jenis_berita = models.CharField(max_length=100)
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    ditulis_oleh = models.CharField(max_length=255)
    banner_berita = models.ImageField(upload_to='berita_banners/')
    def __str__(self):
     return self.judul

class CeritaPendek(models.Model):
    id = models.AutoField(primary_key=True)
    judul = models.CharField(max_length=255)
    isi_cerita = models.TextField()
    pengguna = models.CharField(max_length=255)
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    def __str__(self):
     return self.judul

class Buku(models.Model):
    id = models.AutoField(primary_key=True)
    judul = models.CharField(max_length=255)
    sinopsis = models.TextField()
    penulis = models.CharField(max_length=255)
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    buku_pdf = models.FileField(upload_to='buku_pdfs/')
    def __str__(self):
     return self.judul

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    judul = models.CharField(max_length=255)
    isi = models.TextField()
    nama_pengguna = models.CharField(max_length=255)
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    def __str__(self):
     return self.judul