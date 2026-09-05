from django.urls import path
from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.program_list, name='list'),
    path('<slug:slug>/', views.program_detail, name='detail'),
    path('admin/', views.admin_programs, name='admin_list'),
    path('admin/add/', views.admin_program_add, name='admin_add'),
    path('admin/<int:program_id>/edit/', views.admin_program_edit, name='admin_edit'),
    path('admin/<int:program_id>/delete/', views.admin_program_delete, name='admin_delete'),
]
