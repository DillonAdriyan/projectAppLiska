from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin
# from django.utils.html import format_html
# from .forms import RegistrationForm
from .models import ProfileSiswa

admin.site.register(ProfileSiswa)
#admin.site.register(UserSiswa)
#admin.site.register(CustomUser)
# # Register your models here.
# class UserProfileAdmin(UserAdmin):
#     form = RegistrationForm  # Gunakan formulir yang sudah Anda buat

#     def profile_image(self, obj):
#         return format_html('<img src="{}" width="50" />', obj.profile_picture.url)

#     profile_image.short_description = 'Profile Picture'

#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_picture')

# admin.site.unregister(User)
# admin.site.register(User, UserProfileAdmin)