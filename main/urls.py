from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("buku/", views.buku, name="buku"),
    path("berita/", views.berita, name="berita"),
    path("blog/", views.blog, name="blog"),
    path("cerita/", views.cerpen, name="cerita"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]