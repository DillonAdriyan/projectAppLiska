# Generated by Django 4.2.6 on 2023-11-25 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_userprofile_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo_profile',
            field=models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='photo profile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.customuser'),
        ),
    ]
