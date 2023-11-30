from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register_user, name="register"),
    path("buku/", views.buku, name="buku"),
    path('download/<int:buku_id>/', views.download_buku, name='download_book'),
    path("berita/", views.berita, name="berita"),
    path("blog/", views.blog, name="blog"),
    path("puisi/", views.puisi, name="puisi"),
    path("cerita/", views.cerita, name="cerita"),
    path('login/', views.login_view, name='login'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('puisi/<int:puisi_id>/', views.puisi_detail, name='puisi_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)