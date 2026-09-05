from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DashboardWidget(models.Model):
    WIDGET_TYPES = [
        ('stats', 'Statistics'),
        ('chart', 'Chart'),
        ('recent_activity', 'Recent Activity'),
        ('upcoming_events', 'Upcoming Events'),
        ('pending_tasks', 'Pending Tasks'),
        ('announcements', 'Announcements'),
        ('quick_actions', 'Quick Actions'),
    ]
    
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    config = models.JSONField(default=dict)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.name

class UserDashboardPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_preferences')
    widgets = models.ManyToManyField(DashboardWidget, through='DashboardWidgetUser')
    layout = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Dashboard Preferences"

class DashboardWidgetUser(models.Model):
    widget = models.ForeignKey(DashboardWidget, on_delete=models.CASCADE)
    user_preference = models.ForeignKey(UserDashboardPreference, on_delete=models.CASCADE)
    position = models.JSONField(default=dict)
    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.widget.name} - {self.user_preference.user.username}"
