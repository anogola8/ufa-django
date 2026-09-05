from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('<slug:slug>/', views.project_detail, name='detail'),
    path('create/', views.project_create, name='create'),
    path('<slug:slug>/edit/', views.project_edit, name='edit'),
    path('<slug:slug>/delete/', views.project_delete, name='delete'),
]
