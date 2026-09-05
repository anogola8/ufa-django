from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Executive Dashboard
    path('executive/', views.executive_dashboard, name='executive'),
    path('', views.executive_dashboard, name='index'),
    
    # Member Dashboard
    path('member/', views.member_dashboard, name='member'),
    
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin'),
    
    # Analytics Dashboard
    path('analytics/', views.analytics_dashboard, name='analytics'),
    
    # Reports Dashboard
    path('reports/', views.reports_dashboard, name='reports'),
    
    # API endpoints
    path('api/stats/', views.dashboard_stats_api, name='api_stats'),
    path('api/report/<int:template_id>/', views.generate_report, name='generate_report'),
]
