# Generated by Django 4.2.6 on 2023-10-21 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='banner',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='blog_banners/'),
        ),
    ]
