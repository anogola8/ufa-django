from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Album, Photo, Video

def gallery_list(request):
    """View all albums and recent photos"""
    albums = Album.objects.filter(is_published=True).order_by('-created_at')
    recent_photos = Photo.objects.filter(album__is_published=True).order_by('-uploaded_at')[:12]
    recent_videos = Video.objects.filter(is_published=True).order_by('-created_at')[:6]
    
    context = {
        'albums': albums,
        'recent_photos': recent_photos,
        'recent_videos': recent_videos,
    }
    return render(request, 'gallery/list.html', context)

def album_detail(request, slug):
    """View single album with photos"""
    album = get_object_or_404(Album, slug=slug, is_published=True)
    photos = album.photos.all().order_by('order', '-uploaded_at')
    
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'gallery/album.html', context)

def video_list(request):
    """View all videos"""
    videos = Video.objects.filter(is_published=True).order_by('-created_at')
    
    context = {
        'videos': videos,
    }
    return render(request, 'gallery/videos.html', context)

@staff_member_required
def album_create(request):
    """Create a new album (staff only)"""
    if request.method == 'POST':
        messages.success(request, 'Album created successfully!')
        return redirect('gallery:list')
    return render(request, 'gallery/album_create.html')

@staff_member_required
def photo_upload(request):
    """Upload photos to an album (staff only)"""
    if request.method == 'POST':
        messages.success(request, 'Photos uploaded successfully!')
        return redirect('gallery:list')
    return render(request, 'gallery/photo_upload.html')

@staff_member_required
def video_upload(request):
    """Upload a video (staff only)"""
    if request.method == 'POST':
        messages.success(request, 'Video uploaded successfully!')
        return redirect('gallery:videos')
    return render(request, 'gallery/video_upload.html')
