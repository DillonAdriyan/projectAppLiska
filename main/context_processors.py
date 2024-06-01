from .models import UserProfile
def photo_profile(request):
    photo = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if user_profile:
            photo = user_profile.photo_profile
    return {'photo_profile': photo}
    