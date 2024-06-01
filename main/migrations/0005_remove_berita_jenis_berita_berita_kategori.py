# Generated by Django 4.2.6 on 2023-11-30 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_user_blog_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='berita',
            name='jenis_berita',
        ),
        migrations.AddField(
            model_name='berita',
            name='kategori',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.kategori'),
            preserve_default=False,
        ),
    ]
