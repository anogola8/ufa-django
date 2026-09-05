from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta

# Import all models
from members.models import Member
from events.models import Event, EventRegistration
from news.models import News, Category
from gallery.models import Album, Photo, Video
from projects.models import Project, ProjectUpdate
from leadership.models import Leader
from programs.models import Program
from appointments.models import Appointment

# Import forms
from .forms import (
    MemberForm, EventForm, NewsForm, 
    AlbumForm, PhotoForm, ProjectForm
)

try:
    from leadership.forms import LeaderForm
except ImportError:
    LeaderForm = None


@staff_member_required
def admin_dashboard(request):
    # Main admin dashboard with all management options
    total_leaders = Leader.objects.count() if hasattr(Leader, 'objects') else 0
    active_leaders = Leader.objects.filter(is_active=True).count() if hasattr(Leader, 'objects') else 0
    total_programs = Program.objects.filter(is_active=True).count() if hasattr(Program, 'objects') else 0
    total_appointments = Appointment.objects.count() if hasattr(Appointment, 'objects') else 0

    context = {
        'total_members': Member.objects.count(),
        'pending_members': Member.objects.filter(membership_status='pending').count(),
        'active_members': Member.objects.filter(membership_status='active').count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(start_date__gte=timezone.now(), status='published').count(),
        'total_news': News.objects.count(),
        'published_news': News.objects.filter(status='published').count(),
        'total_projects': Project.objects.count(),
        'active_projects': Project.objects.filter(status__in=['planning', 'ongoing']).count(),
        'total_albums': Album.objects.count(),
        'total_photos': Photo.objects.count(),
        'total_videos': Video.objects.count(),
        'total_leaders': total_leaders,
        'active_leaders': active_leaders,
        'total_programs': total_programs,
        'total_appointments': total_appointments,
        'recent_members': Member.objects.order_by('-joined_date')[:5],
        'recent_events': Event.objects.order_by('-created_at')[:5],
        'recent_news': News.objects.order_by('-publish_date')[:5],
        'recent_projects': Project.objects.order_by('-created_at')[:5],
        'today': timezone.now(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


# ============ MEMBER MANAGEMENT ============
@staff_member_required
def admin_members(request):
    members = Member.objects.all().order_by('-joined_date')
    return render(request, 'dashboard/admin_members.html', {'members': members})


@staff_member_required
def admin_member_add(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully!')
            return redirect('admin_dashboard:members')
    else:
        form = MemberForm()
    return render(request, 'dashboard/admin_member_form.html', {'form': form, 'title': 'Add Member'})


@staff_member_required
def admin_member_edit(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully!')
            return redirect('admin_dashboard:members')
    else:
        form = MemberForm(instance=member)
    return render(request, 'dashboard/admin_member_form.html', {'form': form, 'title': 'Edit Member'})


@staff_member_required
def admin_member_delete(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Member deleted successfully!')
        return redirect('admin_dashboard:members')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': member, 'type': 'Member'})


# ============ EVENT MANAGEMENT ============
@staff_member_required
def admin_events(request):
    events = Event.objects.all().order_by('-start_date')
    return render(request, 'dashboard/admin_events.html', {'events': events})


@staff_member_required
def admin_event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event added successfully!')
            return redirect('admin_dashboard:events')
    else:
        form = EventForm()
    return render(request, 'dashboard/admin_event_form.html', {'form': form, 'title': 'Add Event'})


@staff_member_required
def admin_event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('admin_dashboard:events')
    else:
        form = EventForm(instance=event)
    return render(request, 'dashboard/admin_event_form.html', {'form': form, 'title': 'Edit Event'})


@staff_member_required
def admin_event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('admin_dashboard:events')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': event, 'type': 'Event'})


# ============ NEWS MANAGEMENT ============
@staff_member_required
def admin_news(request):
    news_items = News.objects.all().order_by('-publish_date')
    categories = Category.objects.all()
    return render(request, 'dashboard/admin_news.html', {'news_items': news_items, 'categories': categories})


@staff_member_required
def admin_news_add(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'News article added successfully!')
            return redirect('admin_dashboard:news')
    else:
        form = NewsForm()
    return render(request, 'dashboard/admin_news_form.html', {'form': form, 'title': 'Add News'})


@staff_member_required
def admin_news_edit(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'News updated successfully!')
            return redirect('admin_dashboard:news')
    else:
        form = NewsForm(instance=news)
    return render(request, 'dashboard/admin_news_form.html', {'form': form, 'title': 'Edit News'})


@staff_member_required
def admin_news_delete(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'News deleted successfully!')
        return redirect('admin_dashboard:news')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': news, 'type': 'News'})


# ============ PROJECT MANAGEMENT ============
@staff_member_required
def admin_projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'dashboard/admin_projects.html', {'projects': projects})


@staff_member_required
def admin_project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('admin_dashboard:projects')
    else:
        form = ProjectForm()
    return render(request, 'dashboard/admin_project_form.html', {'form': form, 'title': 'Add Project'})


@staff_member_required
def admin_project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('admin_dashboard:projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'dashboard/admin_project_form.html', {'form': form, 'title': 'Edit Project'})


@staff_member_required
def admin_project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('admin_dashboard:projects')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': project, 'type': 'Project'})


# ============ GALLERY MANAGEMENT ============
@staff_member_required
def admin_gallery(request):
    albums = Album.objects.all().order_by('-created_at')
    photos = Photo.objects.all().order_by('-uploaded_at')[:20]
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'dashboard/admin_gallery.html', {'albums': albums, 'photos': photos, 'videos': videos})


@staff_member_required
def admin_album_add(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Album added successfully!')
            return redirect('admin_dashboard:gallery')
    else:
        form = AlbumForm()
    return render(request, 'dashboard/admin_album_form.html', {'form': form, 'title': 'Add Album'})


@staff_member_required
def admin_album_edit(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, 'Album updated successfully!')
            return redirect('admin_dashboard:gallery')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'dashboard/admin_album_form.html', {'form': form, 'title': 'Edit Album'})


@staff_member_required
def admin_album_delete(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        album.delete()
        messages.success(request, 'Album deleted successfully!')
        return redirect('admin_dashboard:gallery')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': album, 'type': 'Album'})


@staff_member_required
def admin_photo_add(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo added successfully!')
            return redirect('admin_dashboard:gallery')
    else:
        form = PhotoForm()
    return render(request, 'dashboard/admin_photo_form.html', {'form': form, 'title': 'Add Photo'})


@staff_member_required
def admin_photo_delete(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('admin_dashboard:gallery')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': photo, 'type': 'Photo'})


# ============ LEADERSHIP MANAGEMENT ============
@staff_member_required
def admin_leadership(request):
    # Admin view for leadership management
    leaders = Leader.objects.all().order_by('order', '-created_at')
    context = {'leaders': leaders}
    return render(request, 'dashboard/admin_leadership.html', context)


@staff_member_required
def admin_leader_add(request):
    # Add a new leader
    if request.method == 'POST':
        form = LeaderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leader added successfully!')
            return redirect('admin_dashboard:leadership')
    else:
        form = LeaderForm()
    return render(request, 'dashboard/admin_leader_form.html', {'form': form, 'title': 'Add Leader'})


@staff_member_required
def admin_leader_edit(request, leader_id):
    # Edit a leader
    leader = get_object_or_404(Leader, id=leader_id)
    if request.method == 'POST':
        form = LeaderForm(request.POST, request.FILES, instance=leader)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leader updated successfully!')
            return redirect('admin_dashboard:leadership')
    else:
        form = LeaderForm(instance=leader)
    return render(request, 'dashboard/admin_leader_form.html', {'form': form, 'title': 'Edit Leader'})


@staff_member_required
def admin_leader_delete(request, leader_id):
    # Delete a leader
    leader = get_object_or_404(Leader, id=leader_id)
    if request.method == 'POST':
        leader.delete()
        messages.success(request, 'Leader deleted successfully!')
        return redirect('admin_dashboard:leadership')
    return render(request, 'dashboard/admin_confirm_delete.html', {'object': leader, 'type': 'Leader'})
