# Generated by Django 4.2.6 on 2023-11-26 04:17

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('groups', models.ManyToManyField(related_name='custom_user_group', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='custom_user_permission', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Berita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('isi_berita', models.TextField()),
                ('jenis_berita', models.CharField(max_length=100)),
                ('tanggal_upload', models.DateTimeField(auto_now_add=True)),
                ('ditulis_oleh', models.CharField(max_length=255)),
                ('banner_berita', models.ImageField(upload_to='berita_banners/')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('isi', models.TextField()),
                ('tgl_dibuat', models.DateTimeField(auto_now_add=True)),
                ('terakhir_diubah', models.DateTimeField(auto_now=True)),
                ('gambar', models.ImageField(upload_to='blog_banners/')),
            ],
        ),
        migrations.CreateModel(
            name='Buku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('sinopsis', models.TextField()),
                ('penulis', models.CharField(max_length=255)),
                ('tanggal_upload', models.DateTimeField(auto_now_add=True)),
                ('buku_pdf', models.FileField(upload_to='buku_pdfs/')),
            ],
        ),
        migrations.CreateModel(
            name='CeritaPendek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('isi', models.TextField()),
                ('pengguna', models.CharField(max_length=255)),
                ('tanggal_upload', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Puisi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('isi', models.TextField()),
                ('tema', models.CharField(max_length=64)),
                ('penulis', models.CharField(max_length=255)),
                ('tanggal_upload', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('photo_profile', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('typer_user', models.PositiveSmallIntegerField(choices=[(1, 'Siswa'), (2, 'Guru'), (3, 'CEO'), (4, 'Developer'), (5, 'admin')], null=True)),
                ('kelas', models.PositiveSmallIntegerField(choices=[(1, 'X'), (2, 'XI'), (3, 'XII')], null=True)),
                ('jurusan', models.PositiveSmallIntegerField(choices=[(1, 'AKL'), (2, 'APHP'), (3, 'TBSM'), (4, 'TJKT'), (5, 'TKRO'), (6, 'TP')], null=True)),
                ('tanggal_lahir', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileSiswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('profile_picture', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['first_name', 'last_name', 'profile_picture'],
            },
        ),
        migrations.CreateModel(
            name='Comment_Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pengguna', models.CharField(max_length=256)),
                ('isi', models.TextField()),
                ('tgl_dibuat', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.blog')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='kategori',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.kategori'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
