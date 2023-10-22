from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.DashboardBase.as_view(), name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("buku/", views.BukuDashboard.as_view, name="buku"),
    path("berita/", views.BeritaDashboard.as_view, name="berita"),
    path("blog/", views.blog, name="blog"),
    path("puisi/", views.puisi, name="puisi"),
    path("cerita/", views.CerpenDashboard.as_view, name="cerita"),
    path('login/', views.login_view, name='login'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('puisi/<int:puisi_id>/', views.puisi_detail, name='puisi_detail'),

]
