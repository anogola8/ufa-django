from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', include('dashboard.admin_urls')),
    path('', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('projects/', include('projects.urls')),
    path('news/', include('news.urls')),
    path('gallery/', include('gallery.urls')),
    path('events/', include('events.urls')),
    path('leadership/', include('leadership.urls')),
    path('programs/', include('programs.urls')),
    path('appointments/', include('appointments.urls')),
    path('accounts/', include('accounts.urls')),
    
    # Authentication
    path('login/', accounts_views.CustomLoginView.as_view(), name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('register/', accounts_views.register, name='register'),
    path('profile/', accounts_views.profile, name='profile'),
    
    # Custom login (optional)
    path('custom-login/', accounts_views.custom_login, name='custom_login'),
    
    # Password Reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
