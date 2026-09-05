from django.urls import path
from . import admin_views

app_name = 'admin_dashboard'

urlpatterns = [
    # Dashboard
    path('', admin_views.admin_dashboard, name='dashboard'),
    
    # Members
    path('members/', admin_views.admin_members, name='members'),
    path('members/add/', admin_views.admin_member_add, name='member_add'),
    path('members/<int:member_id>/edit/', admin_views.admin_member_edit, name='member_edit'),
    path('members/<int:member_id>/delete/', admin_views.admin_member_delete, name='member_delete'),
    
    # Events
    path('events/', admin_views.admin_events, name='events'),
    path('events/add/', admin_views.admin_event_add, name='event_add'),
    path('events/<int:event_id>/edit/', admin_views.admin_event_edit, name='event_edit'),
    path('events/<int:event_id>/delete/', admin_views.admin_event_delete, name='event_delete'),
    
    # News
    path('news/', admin_views.admin_news, name='news'),
    path('news/add/', admin_views.admin_news_add, name='news_add'),
    path('news/<int:news_id>/edit/', admin_views.admin_news_edit, name='news_edit'),
    path('news/<int:news_id>/delete/', admin_views.admin_news_delete, name='news_delete'),
    
    # Projects
    path('projects/', admin_views.admin_projects, name='projects'),
    path('projects/add/', admin_views.admin_project_add, name='project_add'),
    path('projects/<int:project_id>/edit/', admin_views.admin_project_edit, name='project_edit'),
    path('projects/<int:project_id>/delete/', admin_views.admin_project_delete, name='project_delete'),
    
    # Gallery
    path('gallery/', admin_views.admin_gallery, name='gallery'),
    path('gallery/album/add/', admin_views.admin_album_add, name='album_add'),
    path('gallery/album/<int:album_id>/edit/', admin_views.admin_album_edit, name='album_edit'),
    path('gallery/album/<int:album_id>/delete/', admin_views.admin_album_delete, name='album_delete'),
    path('gallery/photo/add/', admin_views.admin_photo_add, name='photo_add'),
    path('gallery/photo/<int:photo_id>/delete/', admin_views.admin_photo_delete, name='photo_delete'),
    
    # Leadership
    path('leadership/', admin_views.admin_leadership, name='leadership'),
    path('leadership/add/', admin_views.admin_leader_add, name='leader_add'),
    path('leadership/<int:leader_id>/edit/', admin_views.admin_leader_edit, name='leader_edit'),
    path('leadership/<int:leader_id>/delete/', admin_views.admin_leader_delete, name='leader_delete'),
]
