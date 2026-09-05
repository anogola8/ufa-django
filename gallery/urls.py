from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery_list, name='list'),
    path('albums/<slug:slug>/', views.album_detail, name='album'),  # Fixed: added 'albums/' prefix
    path('videos/', views.video_list, name='videos'),
    path('album/create/', views.album_create, name='album_create'),
    path('photo/upload/', views.photo_upload, name='photo_upload'),
    path('video/upload/', views.video_upload, name='video_upload'),
]
