# Generated by Django 4.2.6 on 2023-10-21 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_blog_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='nama_pengguna',
            field=models.CharField(default='User', max_length=255),
        ),
    ]
